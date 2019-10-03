[![Build Status](https://travis-ci.org/Whodiduexpect/assignment-list.svg?branch=master)](https://travis-ci.org/Whodiduexpect/assignment-list)

# Assignment List

**PLEASE NOTE: Assignment list is still very much a work in progress**

Assignment list is an assignment organizing application for students that have a Student Vue web portal. It allows to keep track of a list of assignments and allows you to do things like mark assignments as completed and add new assignments that were not put on Student Vue. New features are planned to be implemented, for example, a reminder that allows you to remind you of a certain assignment on a specific day when you ask for the list of assignments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You will need Python 3.6 or later installed and working for this script to work.

### Installing

Clone the repository

Example: Cloning the repository with Git

    git clone git://github.com/Whodiduexpect/assignment-list.git

Install the dependencies

    pip install -r requirements.txt

Start the script. (In this example, we'll use no arguments just to trigger the setup sequence without actually using it)

    python assignment_list.py

If everything is working, you should see it output:

    First time setup - Please enter your student id number, your password and your district domain separated by commas.

Enter your student id number, your password, and your district domain (the first part of your login URL) separated by commas.
(This is an example)

    123456,mysupersecurepassword,https://portal.somedistrict.us

If you correctly entered your login details, it should output:

    Did you mean to do something? Try adding the argument "--help"

### Demonstration

For this demonstration, let's follow through with that suggestion:

    python assignment_list.py --help

    usage: assignment_list.py [-h] [-c ASSIGNMENT_NUMBER] [-a "ASSIGNMENT TEXT"]
                              [-i "ASSIGNMENT TEXT"] [-l]

    optional arguments:
      -h, --help            show this help message and exit
      -c ASSIGNMENT_NUMBER, --complete ASSIGNMENT_NUMBER
                            Mark an assignment as complete
      -a "ASSIGNMENT TEXT", --add "ASSIGNMENT TEXT"
                            Add an assignment not found in Student Vue
      -i "ASSIGNMENT TEXT", --incomplete "ASSIGNMENT TEXT"
                            Mark a complete assignment as incomplete
      -l, --list            List to do assignments

Now, let's break it down:

- There are five commands
  -"--help" or "-h" which shows this help screen
  - "--complete" or "-c" which completes an assignment
  - "--add" or "-a" which adds an assignment that is not present in Student Vue
  - "--incomplete" or "-i" which marks a complete assignment as incomplete
  - "--list" or "-l" which shows you the assignment list

#### Testing it out

Now let's test out these features.
First off, we check the assignments we have due:

    python assignment_list.py --list

    -- Assignment List --
    1. Test assignment
    2. Algebra assignment from Student Vue

Now that we have the list, we will mark the second one as complete:

    python assignment_list.py --complete 2

    Marked assignment #2 as complete

We then check the list again

    python assignment_list.py -l

    -- Assignment List --
    1. Test assignment

It's gone! Let's try adding an assignment manually

    python assignment_list.py --add "Some assignment that was not added"

    Added assignment "Some assignment that was not added"

To make sure that what we did worked, let's check the list once again

    python assignment_list.py --list

    -- Assignment List --
    1. Some assignment that was not added
    2. Test assignment

Whoops! Turns out that algebra worksheet had a backside... Let's fix that

    python assignment_list.py --incomplete "Algebra assignment from Student Vue"

    Marked assignment "Algebra assignment from Student Vue" as incomplete

And if we pull up the list:

    python assignment_list.py -l

    -- Assignment List --
    1. Some assignment that was not added
    2. Algebra assignment from Student Vue
    3. Test assignment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
