#!/usr/bin/env python3
from studentvue import StudentVue
import sys
import os
import argparse
from pathlib import Path

# Define functions
def open_data(file,mode):
	return open(Path("data/%s" % file), mode)

def list_assignments(assignments):
    if not len(assignments):
        print("No assignments to do!")
    else:
        print("-- Assignment List --")
        i = 0
    for assignment in assignments:
        i += 1
        print(str(i) + ".", assignment)

def update_file(file, list):
    with open_data(file, 'w') as f:
        for assignment in list:
            f.write("%s\n" % assignment)

def get_data_from_file(filename, split_char):
    file = open_data(filename, "r")
    output = file.read().split(split_char)
    file.close()
    return output

def create_if_not_exist(filename):
    if not os.path.exists(Path("data/%s" % filename)):
        file = open_data(filename, "w")
        file.close()

def get_assignments(credentials):
        # Login to Student Vue
    try:
        sv = StudentVue(credentials[0],credentials[1],credentials[2])
    except:
        print("Invalid credentials. Try checking \"data/credentials\" to make sure that it has a valid student id number, password, and district domain, all seperated by commas.")
        sys.exit()

    # Read completed assignments from file
    completed_assignments = get_data_from_file("completed-assignments", "\n")
    # Read added assignments from file
    added_assignments = get_data_from_file("added-assignments", "\n")
    # Get Student Vue assignments
    studentvue_assignments = sv.get_assignments()
    # Merge them all in to one list
    return [x for x in added_assignments + studentvue_assignments if x not in completed_assignments]

# End define functions

# Start
def start():
    # Create files if they don't exist
    if not os.path.exists(Path("data/credentials")): # If there is not a credential file, prompt the user to create one
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
    parser.add_argument("-c", "--complete", metavar = "ASSIGNMENT_NUMBER", help="Mark an assignment as complete", type=int)
    parser.add_argument("-a", "--add", metavar = "\"ASSIGNMENT TEXT\"",help="Add an assignment not found in Student Vue")
    parser.add_argument("-i", "--incomplete", metavar = "\"ASSIGNMENT TEXT\"",help="Mark a complete assignment as incomplete")
    parser.add_argument("-l", "--list", help="List to do assignments", action="store_true")
    args = parser.parse_args()

    if args.list:
        assignments = get_assignments(credentials)
        list_assignments(assignments)
    if args.complete:
        assignments = get_assignments(credentials)
        completed_assignments.append(assignments[args.complete-1])
        update_file('completed-assignments', completed_assignments)
        print("Marked assignment #" + str(args.complete), "as complete" )
    if args.add:
        assignments = get_assignments(credentials)
        added_assignments.append(args.add)
        update_file('added-assignments', added_assignments)
        print("Added assignment \"%s\"" % args.add)
    if args.incomplete:
        assignments = get_assignments(credentials)
        if args.incomplete in completed_assignments:
            completed_assignments.remove(args.incomplete)
            update_file('completed-assignments', completed_assignments)
            print ("Marked assignment \"%s\" as incomplete" % args.incomplete)
        else:
            print("\"%s\" is not a completed assignment." % args.incomplete)
    if not args.add and not args.complete and not args.list and not args.incomplete:
        print("Did you mean to do something? Try adding the argument \"--help\"")

if __name__ == "__main__": # Start only if we're starting the file directely (to avoid breaking tests)
   start()