#!/usr/bin/env python3
import sys
import os
import click
import pandas as pd
from pathlib import Path
import studentvue_parser
import random


# Define functions
def openData(file, mode):
    return open(Path('data/%s' % file), mode)


def listAssignments(assignments):
    if not len(assignments):
        click.echo('No assignments to do!')
    else:
        assignments_view = assignments[assignments['is_completed'] != True]
        assignments_view = assignments_view.drop(columns=['is_completed'])
        click.echo(assignments_view)


def getDataFromFile(filename, split_char):
    file = openData(filename, 'r')
    output = file.read().split(split_char)
    file.close()
    return output


def updateCsv(assignments):
    assignments.to_csv(
        Path('data/studentvue_assignments.csv'),
        sep='/',
        index=False)


def createIfNotExist(filename):
    if not os.path.exists(Path('data/%s' % filename)):
        file = openData(filename, 'w')
        file.close()


def pointProblematicFile(path):
    click.echo('Full path to problematic file: %s' % Path(path).absolute())


# Main
def main():
    # If the credential file does not exist:
    if not os.path.exists(Path('data/studentvue_credentials')):
        # If we don't even have a data folder:
        if not os.path.exists('data'):
            # Create one
            os.mkdir('data')
        # Now that we know we have a data folder, let's set the credentials
        studentvue_parser.setCredentials()

    # Read the credential file
    credentials = getDataFromFile('studentvue_credentials', ',')

    # Define commands
    @click.group()
    def cli():
        '''
        A better Student Vue assignment manager, (c) 2019 Whodiduexpect
        '''

    @cli.command()
    def reset():
        '''
        Reset credentials
        '''
        studentvue_parser.setCredentials()

    @cli.command()
    @click.argument('category', required=False)
    def list(category):
        '''
        List assignments by CATEGORY (defaults to 'current')
        '''
        if not category:
            category = 'current'
        if category == 'current':
            assignments = studentvue_parser.getAssignments(credentials)
            listAssignments(assignments)
        else:
            click.echo(
                '"%s" is not a valid category. Currently, the only valid category is current' %
                category)

    @cli.command()
    @click.argument('id')
    def complete(id):
        '''
        Complete an assignment by assignment ID
        '''
        assignments = studentvue_parser.getAssignments(credentials)
        try:
            assignments.at[assignments.loc[assignments['Assignment ID'].isin(
                [id])].index, 'is_completed'] = True
            updateCsv(assignments)
        except BaseException:
            click.echo('Failed to complete assignemnt #%s' % id)
            sys.exit()
        click.echo('Marked assignment #%s as complete' % id)

    @cli.command()
    @click.argument('title')
    @click.argument('date')
    def add(title, date):
        '''
        Add a new assignment with the TITLE and DATE
        '''
        # Get schedule
        classes = studentvue_parser.getSchedule(credentials)
        # Print all the classes
        for class_ in classes:
            print(class_)
        # Ask for which period
        class_period_input = input(
            '\nWhich class period do you want to add the assignment "%s" to? ' %
            title)
        class_period = int(class_period_input)

        # Auto generate the class as if it was from Student Vue
        teacher_fullname = classes[class_period - 1].teacher.name.split(' ')
        teacher_label = "{0}, {1}".format(
            teacher_fullname[1], teacher_fullname[0][:1])
        class_name = "{0}  {1}({2})".format(teacher_label,
                                            classes[class_period - 1].name,
                                            classes[class_period - 1].period)

        # Generate a assignment list 8 digit id, and make sure it's unique
        assignments = studentvue_parser.getAssignments(credentials)
        id_unique = False

        while not id_unique:
            generated_id = random.randrange(11111111, 99999999, 1)
            is_id_unique = True
            for assignment_id in assignments["Assignment ID"]:
                if assignment_id == generated_id:
                    is_id_unique = False
            if is_id_unique:
                id_unique = True

        assignment_df = pd.DataFrame({'Assignment ID': [generated_id], 'Class Name': [
                                     class_name], 'Due Date': [date], 'Assignment': [title], 'is_completed': ['False']})
        assignments = assignments.append(assignment_df, sort=True)
        convert_dict = {'Assignment ID': int}
        assignments = assignments.astype(convert_dict)
        updateCsv(assignments)
        print(assignments)
    # Execute command
    cli(obj={})


if __name__ == '__main__':
    main()
