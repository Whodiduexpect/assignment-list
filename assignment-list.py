#!/usr/bin/env python3
from studentvue import StudentVue
import sys
import os
import argparse
from pathlib import Path

def open_data(file,mode):
	return open(Path("data/%s" % file), mode)

# Create files if they don't exist
if not os.path.exists(Path("data/credentials")): # If there is not a credential file, prompt the user to create one
	if not os.path.exists("data"):
		os.mkdir("data")
	print("First time setup - Please enter your student id number, your password and your district domain seperated by commas.")
	credentials = input()
	file = open_data("credentials", "w")
	file.write(credentials)
	file.close()
if not os.path.exists(Path("data/completed-assignments")):
	file = open_data(Path("completed-assignments"), "w")
if not os.path.exists(Path("data/added-assignments")):
	file = open_data(Path("added-assignments"), "w")

# Read the credential file
file = open_data("credentials", "r")
credentials = file.read().split(',')
file.close()

# Login to Student Vue
try:
	sv = StudentVue(credentials[0],credentials[1],credentials[2])
except:
	print("Invalid credentials. Try checking the \"credentials\" file to make sure that it has a valid student id number, password, and district domain, all seperated by commas.")

# Read completed assignments from file
file = open_data("completed-assignments", "r")
completed_assignments = file.read().split('\n')
file.close()
# Read added assignments from file
file = open_data("added-assignments", "r")
added_assignments = file.read().split('\n')
file.close()
# Get Student Vue assignments
studentvue_assignments = sv.get_assignments()
# Merge them all in to one list
assignments = [x for x in added_assignments + studentvue_assignments if x not in completed_assignments]

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--complete", metavar = "ASSIGNMENT_NUMBER", help="Mark an assignment as complete", type=int)
parser.add_argument("-a", "--add", metavar = "\"ASSIGNMENT TEXT\"",help="Add an assignment not found in Student Vue")
parser.add_argument("-l", "--list", help="List to do assignments", action="store_true")
args = parser.parse_args()

if args.list:
	if not len(assignments):
		print("No assignments to do!")
	else:
		print("-Assignment List-")
		i = 0
		for assignment in assignments:
			i += 1
			print(str(i) + ".", assignment)
if args.complete:
	completed_assignments.append(assignments[args.complete-1])
	with open_data('completed-assignments', 'w') as f:
		for assignment in completed_assignments:
		   f.write("%s\n" % assignment)
	print("Marked assignment #" + str(args.complete), "as complete" )
if args.add:
	added_assignments.append(args.add)
	with open_data('added-assignments', 'w') as f:
		for assignment in added_assignments:
		   f.write("%s\n" % assignment)
	print("Added assignment \"%s\"" % args.add)
if not args.add or not args.complete or not args.list:
    print("Did you mean to do something? Try adding the argument \"--help\"")