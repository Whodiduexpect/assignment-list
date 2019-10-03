#!/usr/bin/env python3
import sys
import os
import click
import pandas as pd
from pathlib import Path
import studentvue_parser


# Define functions

def openData(file, mode):
    return open(Path("data/%s" % file), mode)


def listAssignments(assignments):
    if not len(assignments):
        click.echo("No assignments to do!")
    else:
        assignments_view = assignments[assignments["is_completed"] != True]
        assignments_view = assignments_view.drop(columns=["is_completed"])
        click.echo(assignments_view)


def getDataFromFile(filename, split_char):
    file = openData(filename, "r")
    output = file.read().split(split_char)
    file.close()
    return output


def updateCsv(assignments):
    assignments.to_csv(
        Path('data/studentvue_assignments.csv'),
        sep="/",
        index=False)


def createIfNotExist(filename):
    if not os.path.exists(Path("data/%s" % filename)):
        file = openData(filename, "w")
        file.close()


def pointProblematicFile(path):
    click.echo("Full path to problematic file: %s" % Path(path).absolute())


def setVerbose():
    verbose_enabled = True
    click.echo('Verbose mode is on')


# Main
def main():
    # Create files if they don't exist
    # If there is not a credential file, prompt the user to create one
    if not os.path.exists(Path("data/studentvue_credentials")):
        if not os.path.exists("data"):
            os.mkdir("data")
        studentvue_parser.setCredentials()

    # Read the credential file
    credentials = getDataFromFile("studentvue_credentials", ",")

    # Define Commands
    verbose_enabled = False

    @click.group()
    @click.option('--verbose/--no-verbose', default=False)
    def cli(verbose):
        if verbose:
            setVerbose()

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
        List assignments
        '''
        if not category:
            category = "current"
        if category == "current":
            assignments = studentvue_parser.getAssignments(credentials)
            listAssignments(assignments)
        elif category == "past":
            print("Specifically viewing past assignments is not yet available")
        else:
            print("\"%s\" is not a valid category. The valid categories are current and past." % category)

    @cli.command()
    @click.argument('id')
    def complete(id):
        '''
        Complete an assignment
        '''
        assignments = studentvue_parser.getAssignments(credentials)
        assignments.set_value(assignments.loc[assignments['Assignment ID'].isin([id])].index, 'is_completed', True)  # TODO: set_value() is deprecated and will need to be replaced
        updateCsv(assignments)
        click.echo("Marked assignment #%s as complete" % id)

    # Execute command
    cli(obj={})

if __name__ == "__main__":
    main()
