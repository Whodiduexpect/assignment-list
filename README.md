# Assignment List

Assignment list is an assignment organizing application for students that have a Student Vue web portal. It allows to keep track of a list of assignments, and allows you to do things like mark assignments as completed and add new assignments that were not put on Student Vue. New features are planned to be implemented, for example, a reminder that allows you to remind you of a certain assignment on a specific day when you ask for the list of assignments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You will need Python 3 installed and working for this script to work.

### Installing

Clone the repository<br>
Example: Cloning the repository with Git
```
git clone git://github.com/Whodiduexpect/assignment-list.git
```

Install the dependencies

```
pip install -r requirements.txt
```

Start the script. (In this example, we'll use no arguments just to trigger the setup sequence without actually using it)

```
python assignment-list.py
```

If everything is working, you should see it output:
```
First time setup - Please enter your student id number, your password and your district domain seperated by commas.
```
Enter your student id number, your password, and your district domain (the first part of your login url) seperated by commas.
(This is an example)
```
123456,mysupersecurepassword,https://portal.somedistrict.us
```
If you correctly entered your login details, it should output:
```
Did you mean to do something? Try adding the argument "--help"
```
### Demonstration
If you follow through with the program's suggestion you would type this:
```
python assignment-list.py --help
```
And the program would output this:
```
usage: assignment-list.py [-h] [-c ASSIGNMENT_NUMBER] [-a "ASSIGNMENT TEXT"]
                          [-l]

optional arguments:
  -h, --help            show this help message and exit
  -c ASSIGNMENT_NUMBER, --complete ASSIGNMENT_NUMBER
                        Mark an assignment as complete
  -a "ASSIGNMENT TEXT", --add "ASSIGNMENT TEXT"
                        Add an assignment not found in Student Vue
  -l, --list            List to do assignments
```
Now, let's break it down:
* There are four commands
	- "--help" or "-h" which shows this help screen
	- "--complete" or "-c" which completes an assignment
	- "--add" or "-a" which adds an assignment that is not present in Student Vue
	- "--list" or "-l" which shows you the assignment list
#### Testing it out
Now let's test out these features.
First off, we check the assignments we have due:
```
python assignment-list.py --list
```
```
-Assignment List-
1. Test assignment
2. Some other assignment from student vue
```
Now that we have the list, we mark the second one as complete:
```
python assignment-list.py --complete 2
```
```
Marked assignment #2 as complete
```
We then check the list again
```
python assignment-list.py -l
```
```
-Assignment List-
1. Test assignment
```
It's gone! Well I do need to add that assignment that was never added to Student Vue for some reason
```
python assignment-list.py --add "Some assignment that was not added"
```
```
Added assignment "Some assignment that was not added"
```
To make sure that what we did worked, let's check the list once again
```
python assignment-list.py --list
```
```
1. Some assignment that was not added
2. Test assignment
```
This sums up the entire script

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
