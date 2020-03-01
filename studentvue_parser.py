import sys
from getpass import getpass
from pathlib import Path

import click
import pandas as pd
from studentvue import StudentVue

import assignment_list


def set_credentials():
    assignment_list.create_if_not_exist('studentvue_credentials')
    click.echo('-- Credentials setup/reset --')
    student_id = input('Please enter Student ID: ')
    password = getpass('Please enter password (hidden): ')
    district_url = input('Please enter district login url: ')
    file = assignment_list.open_data('studentvue_credentials', 'w')
    file.write(student_id + ',' + password + ',' + district_url)
    file.close()
    return True


def get_stored_assignment_data():
    # Create CSV file if it doesn't exist
    assignment_list.create_if_not_exist('studentvue_assignments.csv')
    try:
        stored_assignments = pd.read_csv(Path('data/studentvue_assignments.csv'),
                                         sep='/')
    except pd.io.common.EmptyDataError:
        stored_assignments = pd.DataFrame({'Assignment ID': [], 'Class Name': [], 'Due Date': [
        ], 'Assignment': [], 'is_completed': []})
        click.echo('Invalid or empty file detected... discarding file')
    convert_dict = {'Assignment ID': int}
    stored_assignments = stored_assignments.astype(convert_dict)
    return stored_assignments


def get_assignments(credentials):
    assignments = get_stored_assignment_data()
    # Login to Student Vue
    try:
        sv = StudentVue(credentials[0], credentials[1], credentials[2])
    except IndexError:
        click.echo(
            'Invalid credentials. You might want to use:\n   python assignment_list.py reset')
        sys.exit()
    try:
        studentvue_assignments = sv.get_assignments()
    except Exception:
        click.echo(
            'Failed to get Student Vue assignments... Please see https://github.com/kajchang/StudentVue for help on '
            'this issue.')
        sys.exit()
    found_duplicate = False
    for sv_assignment in studentvue_assignments:
        setattr(sv_assignment, 'date', str(sv_assignment.date.day) + '/' +
                str(sv_assignment.date.month) + '/' + str(sv_assignment.date.year))
        for assignment_id in assignments['Assignment ID']:
            if sv_assignment.assignment_id == assignment_id:
                found_duplicate = True
        if not found_duplicate:
            assignment_df = pd.DataFrame(
                {
                    'Assignment ID': [
                        sv_assignment.assignment_id], 'Class Name': [
                        sv_assignment.class_name], 'Due Date': [
                        sv_assignment.date], 'Assignment': [
                        sv_assignment.name], 'is_completed': ['False']})
            assignments = assignments.append(assignment_df, sort=True)
    convert_dict = {'Assignment ID': int}
    assignments = assignments.astype(convert_dict)
    assignment_list.update_csv(assignments)
    return assignments


def get_schedule(credentials):
    # Login to Student Vue
    try:
        sv = StudentVue(credentials[0], credentials[1], credentials[2])
    except IndexError:
        click.echo(
            'Invalid credentials. You can reset your credentials with:\n   python assignment_list.py reset')
        sys.exit()
    return sv.get_schedule()


if __name__ == '__main__':
    click.echo("Don't run me! Run assignment_list.py instead.")
