#!/usr/bin/env python3
import os
import random
import sys
from pathlib import Path
import datetime

import click
import pandas as pd

import studentvue_parser

# Exception Handler


def exceptionHandler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if debug_mode:
        print('\n*** Error:')
        debug_hook(exception_type, exception, traceback)
    else:
        print("\t%s: %s" % (exception_type.__name__, exception))

# Define functions


def open_data(file, mode):
    try:
        return open(Path('data/{}'.format(file)), mode)
    except IOError as e:
        raise IOError(
            "A file error has occurred: {}\nConsider checking your file permissions.".format(e))


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
    if not os.path.exists(Path('data/{}'.format(filename))):
        file = open_data(filename, 'w')
        file.close()


# Define commands
@click.group()
@click.option('--debug/--no-debug', default=False, help="Enable/disable debug mode.")
def cli(debug):
    """
    A Student Vue assignment manager

    Copyright (C) 2019-2020 Whodiduexpect
    """
    global debug_mode
    debug_mode = debug


@cli.command()
def reset():
    """
    Reset Student Vue credentials.
    """
    studentvue_parser.set_credentials()


@cli.command()
def update():
    """
    Update database with the latest data from Student Vue.
    """
    click.echo("Updating local assignment database...")
    credentials = get_data_from_file('studentvue_credentials', ',')
    assignments = studentvue_parser.get_assignments(credentials)
    update_csv(assignments)
    click.echo("Synced assignments successfully.")


@cli.command()
@click.argument('category', required=False)
def list(category):
    """
    List assignments by CATEGORY (defaults to 'current').
    """
    if not category:
        category = 'current'
    if category == 'current':
        assignments = studentvue_parser.get_stored_assignment_data()
        list_assignments(assignments)
    elif category == 'completed':
        assignments = studentvue_parser.get_stored_assignment_data()
        list_completed(assignments)
    elif category == 'added':
        assignments = studentvue_parser.get_stored_assignment_data()
        list_added(assignments)
    else:
        click.echo(
            '"{}" is not a valid category. The categories are "current" and "completed"'.format(category))


@cli.command()
@click.argument('id')
def complete(id):
    """
    Complete an assignment by assignment ID.
    """
    assignments = studentvue_parser.get_stored_assignment_data()
    assignments.at[assignments.loc[assignments['Assignment ID'].isin(
        [id])].index, 'is_completed'] = True
    update_csv(assignments)
    click.echo('Marked assignment #{} as complete'.format(id))


@cli.command()
@click.argument('id')
def incomplete(id):
    """
    Mark an assignment as incomplete by assignment ID.
    """
    assignments = studentvue_parser.get_stored_assignment_data()
    assignments.at[assignments.loc[assignments['Assignment ID'].isin(
        [id])].index, 'is_completed'] = False
    update_csv(assignments)
    click.echo('Marked assignment #{} as incomplete'.format(id))


@cli.command()
@click.argument('title')
@click.argument('date')
@click.argument('period')
def add(title, date, period):
    """
    Add a new assignment with the TITLE and DATE (YYYY-MM-DD).
    """
    try:
        # Verify format by attempting to strip time
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError(
            "Date provided '{}' is not in valid ISO 8601 format (YYYY-MM-DD).".format(date))

    credentials = get_data_from_file('studentvue_credentials', ',')
    classes = studentvue_parser.get_schedule(credentials)
    try:
        period = int(period)
    except ValueError:
        raise ValueError(
            "Period provided '{}' is not a valid number".format(period))

    if period > len(classes) or period < 1:
        raise ValueError(
            "Period provided '{}' is not a valid class period (1-{}).".format(period, len(classes)))

    # Auto generate the class name as if it was from Student Vue
    teacher_fullname = classes[period - 1].teacher.name.split(' ')
    teacher_label = '{}, {}'.format(
        teacher_fullname[1], teacher_fullname[0][:1])
    class_name = '{}  {}({})'.format(teacher_label,
                                        classes[period - 1].name,
                                        classes[period - 1].period)

    # Generate a assignment list 8 digit id, and make sure it's unique
    assignments = studentvue_parser.get_stored_assignment_data()
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
    click.echo('Successfully added assignment "{}"'.format(title))


def main():
    # Checking that the credentials are all good
    if not os.path.exists(Path('data/studentvue_credentials')):
        if not os.path.exists('data'):
            try:
                os.mkdir('data')
            except IOError as e:
                raise IOError(
                    "Failed to create data folder: {}\nTry checking your file permissions.".format(e))
        studentvue_parser.set_credentials()
    # Execute commands passed through CLI
    cli(obj={})


if __name__ == '__main__':
    sys.excepthook = exceptionHandler  # Use custom exception handler
    main()
