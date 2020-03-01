#!/usr/bin/env python3
import os
import random
import sys
from pathlib import Path

import click
import pandas as pd

import studentvue_parser


# Define functions
def open_data(file, mode):
    return open(Path('data/%s' % file), mode)


def list_assignments(assignments):
    assignments_view = assignments[assignments['is_completed'] != True]
    assignments_view = assignments_view.drop(columns=['is_completed'])
    if assignments_view.empty:
        click.echo('No assignments to do!')
    else:
        click.echo(assignments_view)


def list_completed(assignments):
    assignments_view = assignments[assignments['is_completed']]
    assignments_view = assignments_view.drop(columns=['is_completed'])
    if assignments_view.empty:
        click.echo('No assignments completed yet.')
    else:
        click.echo(assignments_view)


def list_added(assignments):
    assignments_view = assignments.drop(columns=['is_completed'])
    assignments_view['Assignment ID'] = assignments['Assignment ID'].astype(
        'str')
    mask = (assignments_view['Assignment ID'].str.len() == 8)
    assignments_view = assignments_view.loc[mask]
    if assignments_view.empty:
        click.echo('No assignments added yet.')
    else:
        click.echo(assignments_view)


def get_data_from_file(filename, split_char):
    file = open_data(filename, 'r')
    output = file.read().split(split_char)
    file.close()
    return output


def update_csv(assignments):
    assignments.to_csv(
        Path('data/studentvue_assignments.csv'),
        sep='/',
        index=False)


def create_if_not_exist(filename):
    if not os.path.exists(Path('data/%s' % filename)):
        file = open_data(filename, 'w')
        file.close()


# Define commands
@click.group()
def cli():
    """
    A Student Vue assignment manager
    """


@cli.command()
def reset():
    """
    Reset credentials
    """
    studentvue_parser.set_credentials()


@cli.command()
@click.argument('category', required=False)
def list(category):
    """
    List assignments by CATEGORY (defaults to 'current')
    """
    if not category:
        category = 'current'
    if category == 'current':
        credentials = get_data_from_file('studentvue_credentials', ',')
        assignments = studentvue_parser.get_assignments(credentials)
        list_assignments(assignments)
    elif category == 'completed':
        assignments = studentvue_parser.get_stored_assignment_data()
        list_completed(assignments)
    elif category == 'added':
        assignments = studentvue_parser.get_stored_assignment_data()
        list_added(assignments)
    else:
        click.echo(
            '"%s" is not a valid category. The categories are "current" and "completed"' %
            category)


@cli.command()
@click.argument('id')
def complete(id):
    """
    Complete an assignment by assignment ID
    """
    credentials = get_data_from_file('studentvue_credentials', ',')
    assignments = studentvue_parser.get_assignments(credentials)
    try:
        assignments.at[assignments.loc[assignments['Assignment ID'].isin(
            [id])].index, 'is_completed'] = True
        update_csv(assignments)
    except Exception:
        click.echo('Failed to complete assignment #%s' % id)
        sys.exit()
    click.echo('Marked assignment #%s as complete' % id)


@cli.command()
@click.argument('id')
def incomplete(id):
    """
    Mark an assignment as incomplete by assignment ID
    """
    credentials = get_data_from_file('studentvue_credentials', ',')
    assignments = studentvue_parser.get_assignments(credentials)
    try:
        assignments.at[assignments.loc[assignments['Assignment ID'].isin(
            [id])].index, 'is_completed'] = False
        update_csv(assignments)
    except Exception:
        click.echo('Failed to mark assignment #%s as incomplete' % id)
        sys.exit()
    click.echo('Marked assignment #%s as incomplete' % id)


@cli.command()
@click.argument('title')
@click.argument('date')
def add(title, date):
    """
    Add a new assignment with the TITLE and DATE
    """

    # Get schedule
    credentials = get_data_from_file('studentvue_credentials', ',')
    classes = studentvue_parser.get_schedule(credentials)
    valid = False
    while not valid:
        # Print all the classes
        for class_ in classes:
            print(class_)

        # Ask which period to add the assignment to
        class_period_input = input(
            '\nWhich class period do you want to add the assignment "%s" to? ' %
            title)
        try:  # Check if the input can even be converted to an integer!
            class_period = int(class_period_input)
        except ValueError:
            click.echo('"%s" is an invalid input' % class_period)
        # Check that if the input is an integer, that it is a valid period
        if class_period > len(classes) or class_period < 1:
            click.echo("Invalid period.\n")
        else:
            valid = True

    # Auto generate the class name as if it was from Student Vue
    teacher_fullname = classes[class_period - 1].teacher.name.split(' ')
    teacher_label = '{0}, {1}'.format(
        teacher_fullname[1], teacher_fullname[0][:1])
    class_name = '{0}  {1}({2})'.format(teacher_label,
                                        classes[class_period - 1].name,
                                        classes[class_period - 1].period)

    # Generate a assignment list 8 digit id, and make sure it's unique
    credentials = get_data_from_file('studentvue_credentials', ',')
    assignments = studentvue_parser.get_assignments(credentials)
    id_unique = False

    while not id_unique:
        generated_id = random.randrange(11111111, 99999999, 1)
        is_id_unique = True
        for assignment_id in assignments["Assignment ID"]:
            if assignment_id == generated_id:
                is_id_unique = False
        if is_id_unique:
            id_unique = True

    # Make the assignment based on data we have collected/generated
    assignment_df = pd.DataFrame({'Assignment ID': [generated_id], 'Class Name': [
        class_name], 'Due Date': [date], 'Assignment': [title], 'is_completed': ['False']})
    assignments = assignments.append(assignment_df, sort=True)
    convert_dict = {'Assignment ID': int}
    assignments = assignments.astype(convert_dict)
    update_csv(assignments)
    click.echo('Successfully added assignment "{0}"'.format(title))


def main():
    # If the credential file does not exist:
    if not os.path.exists(Path('data/studentvue_credentials')):
        # If we don't even have a data folder:
        if not os.path.exists('data'):
            # Create one
            os.mkdir('data')
        # Now that we know we have a data folder, let's set the credentials
        studentvue_parser.set_credentials()

    # Execute command
    cli(obj={})


if __name__ == '__main__':
    main()
