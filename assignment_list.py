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


# Main
def main():
    # If the credential file does not exist:
    if not os.path.exists(Path("data/studentvue_credentials")):
        # If we don't even have a data folder:
        if not os.path.exists("data"):
            # Create one
            os.mkdir("data")
        # Now that we know we have a data folder, let's set the credentials
        studentvue_parser.setCredentials()

    # Read the credential file
    credentials = getDataFromFile("studentvue_credentials", ",")

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
        List assignments by CATEGORY (defaults to "current")
        '''
        if not category:
            category = "current"
        if category == "current":
            assignments = studentvue_parser.getAssignments(credentials)
            listAssignments(assignments)
        else:
            click.echo(
                "\"%s\" is not a valid category. The only valid category is current" %
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
                [id])].index, "is_completed"] = True
            updateCsv(assignments)
        except BaseException:
            click.echo("Failed to complete assignemnt #%s" % id)
            sys.exit()
        click.echo("Marked assignment #%s as complete" % id)

    # Execute command
    cli(obj={})


if __name__ == "__main__":
    main()
