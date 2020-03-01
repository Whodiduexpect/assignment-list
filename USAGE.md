# Introduction

Running `python assignment_list.py` or `python assignment_list.py --help` shows a help message:
```
Usage: assignment_list.py [OPTIONS] COMMAND [ARGS]...

  A Student Vue assignment manager

Options:
  --help  Show this message and exit.

Commands:
  add         Add a new assignment with the TITLE and DATE
  complete    Complete an assignment by assignment ID
  incomplete  Mark an assignment as incomplete by assignment ID
  list        List assignments by CATEGORY (defaults to 'current')
  reset       Reset credentials
```
As you can see, there are 5 commands:
* add
* complete
* incomplete
* list
* reset
 
You can get a help message for each command by typing:
 `python assignment_list.py COMMAND --help`
 For example for the command add:

```
python assignment_list.py add --help
```
```
Usage: assignment_list.py add [OPTIONS] TITLE DATE

  Add a new assignment with the TITLE and DATE

Options:
  --help  Show this message and exit.
```

# The `add` command

The `add` command adds an assignment to your list. It accepts the parameters `title` and `date`, it then asks you which period to add it to. If your title is more than a word long, you need to surround it with quotation marks.
Please note that the add command assigns an 8 digit number to the assignment, rather than the 7 digit Student Vue ID.
## Example usage
```
python assignment_list.py add "Assignment Title" 1/1/2019
```
```
Period 1 TESTCLASS I Taught by Test Teacher in Room 0
Period 2 TESTCLASS II Taught by Test Teacher in Room 0
Period 3 TESTCLASS III Taught by Test Teacher in Room 0
Period 4 TESTCLASS IV Taught by Test Teacher in Room 0
Period 5 TESTCLASS V Taught by Test Teacher in Room 0
Period 6 TESTCLASS VI Taught by Test Teacher in Room 0
Period 7 TESTCLASS VII Taught by Test Teacher in Room 0

Which class period do you want to add the assignment "Assignment Title" to? 
```
```
Which class period do you want to add the assignment "Assignment Title" to? 1
```
```
Successfully added assignment "Assignment Title"
```

# The `complete` command

The `complete` command completes an assignment and hides it from the regular list. It takes the `ID` of the assignment as a parameter. This command is meant to be used after seeing the list of assignments.
 ## Example Usage
 ```
 python assignment_list.py complete 1111111
 ```
```
Marked assignment #1111111 as complete
```

# The `incomplete` command
 The `incomplete` command marks an assignment as incomplete and reveals it to the regular list again. It takes the `ID` of the assignment as a parameter. This command is meant to be used after viewing the list of completed assignments (can be viewed with `python assignment_list.py list completed`)
 ## Example Usage
 ```
 python assignment_list.py incomplete 1111111
 ```
 ```
 Marked assignment #1111111 as incomplete
 ```
 
# The `list` command
The `list` command lists the assignments. Currently, it has 3 optional categories, which are `current`, `completed`, and `added` (assignments added via the `add` command). The reason these categories are optional is that by default it's `current`, as to not require an unnecessary long command.
## Example Usage
`python assignment_list.py list` or `python assignment_list.py list current`
```
                                        Assignment  Assignment ID                  Class Name    Due Date
0                               Test Assignment #1        1111111     Last, F  TESTCLASS I(1)   1/01/2019
1                               Test Assignment #2        2222222    Last, F  TESTCLASS II(2)   1/01/2019
2                               Test Assignment #3        3333333   Last, F  TESTCLASS III(3)   1/01/2019
```

# The `reset` command
The `reset` command resets the student vue credentials in the event that they are incorrect or you want to switch accounts.

## Example Usage
```
python assignment_list.py reset
```
```
-- Credentials setup/reset --
Please enter Student ID: 123456
Please enter password (hidden): 
Please enter district login url: https://sis-portal.somedistrict.us
```
