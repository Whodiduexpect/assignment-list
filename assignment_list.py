#!/usr/bin/env python3
from studentvue import StudentVue
import sys
import os
import argparse
from pathlib import Path
import csv


# Define functions
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def open_data(file, mode):
    return open(Path("data/%s" % file), mode)


def list_assignments(assignments):
    if not len(assignments):
        print("No assignments to do!")
    else:
        print("--------------------- Assignment List ---------------------")
        print("ASSGN ID  CLASS                        ASSGN       DUE DATE")
    for assignment in assignments:
        if not assignment.is_completed:
            print(str(assignment.assignment_id) + ":", assignment.class_name,
                  "-", assignment.name, "(Due on %s)" % assignment.date)


def get_data_from_file(filename, split_char):
    file = open_data(filename, "r")
    output = file.read().split(split_char)
    file.close()
    return output


def update_csv(assignments):
    # writes 'assignment_id', 'class_name', 'date', 'name', 'is_completed'
    with open(Path('data/assignments.csv'), mode='w', newline='') as assignments_file:
        csv_writer = csv.writer(
            assignments_file, delimiter='/', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for assignment in assignments:
            csv_writer.writerow([assignment.assignment_id, assignment.class_name,
                                 assignment.date, assignment.name, assignment.is_completed])


def create_if_not_exist(filename):
    if not os.path.exists(Path("data/%s" % filename)):
        file = open_data(filename, "w")
        file.close()


def point_problematic_file(path):
    print("Full path to problematic file: %s" % Path(path).absolute())


def get_assignments(credentials):
    # Login to Student Vue
    try:
        sv = StudentVue(credentials[0], credentials[1], credentials[2])
    except:
        print("Invalid credentials. Try checking %s to make sure that it has a valid student id number, password, and district domain, all seperated by commas." % Path("data/credentials"))
        point_problematic_file("data/credentials")
        sys.exit()

    # Create CSV file if it dosen't exist
    create_if_not_exist("assignments.csv")

    with open(Path("data/assignments.csv")) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='/')
        assignments = []
        try:
            for row in csv_reader:  # reads 'assignment_id', 'class_name', 'date', 'name', 'is_completed'
                current_assignment = Bunch(assignment_id=int(
                    row[0]), class_name=row[1], date=row[2], name=row[3], is_completed=row[4] in "True")
                assignments.append(current_assignment)
        except:
            print("Error parsing %s, please check if there is a formatting issue" % Path(
                "data/assignments.csv"))
            point_problematic_file("data/assignments.csv")
            sys.exit()
    try:
        studentvue_assignments = sv.get_assignments()
    except:
        print("Failed to get Student Vue assignments... Please see https://github.com/kajchang/StudentVue for help on this issue.")
        sys.exit()
    found_duplicate = False
    for sv_assignment in studentvue_assignments:
        setattr(sv_assignment, 'is_completed', False)
        setattr(sv_assignment, 'date', str(sv_assignment.date.day) + "-" +
                str(sv_assignment.date.month) + "-" + str(sv_assignment.date.year))
        for assignment in assignments:
            if sv_assignment.assignment_id == assignment.assignment_id:
                found_duplicate = True
        if not found_duplicate:
            assignments.append(sv_assignment)
    update_csv(assignments)
    return assignments


# Start
def start():
    # Create files if they don't exist
    # If there is not a credential file, prompt the user to create one
    if not os.path.exists(Path("data/credentials")):
        if not os.path.exists("data"):
            os.mkdir("data")
        print("First time setup - Please enter your student id number, your password and your district domain seperated by commas.")
        credentials = input()
        file = open_data("credentials", "w")
        file.write(credentials)
        file.close()
    create_if_not_exist("completed-assignments")
    create_if_not_exist("added-assignments")
    # Read the credential file
    credentials = get_data_from_file("credentials", ",")

    # Get and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--complete", metavar="ASSIGNMENT_NUMBER",
                        help="Mark an assignment as complete", type=int)
    parser.add_argument(
        "-l", "--list", help="List to do assignments", action="store_true")
    args = parser.parse_args()

    if args.list:
        assignments = get_assignments(credentials)
        list_assignments(assignments)
    if args.complete:
        assignments = get_assignments(credentials)
        setattr(assignments, 'is_completed', True)
        print("Marked assignment #" + str(args.complete), "as complete")
    if not args.complete and not args.list:
        print("Did you mean to do something? Try adding the argument \"--help\"")


# Start only if we're starting the file directely (to avoid breaking tests)
if __name__ == "__main__":
    start()
