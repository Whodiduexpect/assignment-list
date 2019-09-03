# What is assignment list?
Assignment list was created because of districts that put all their assignments in a Student Vue web portal. If you don't know Student Vue, this might sound great as it puts all the assignments in one place. 
## Why Student Vue is unfit for assignments
However, Student Vue is poorly designed when it comes to assignments. The only thing it has to offer is a simple calendar with the name of the assignment. That's it - there are no organization tools, you just have to remember which ones you have done, and you can't manually add anything. You can't even filter any assignments, so every time you want to take a look you have to look at every assignment that month. And if it's the last day of the month you have to go all the way to next month just for one day.
## What does assignment list do to help?
It's easy, **all** your assignments are in one quick to access place. This includes assignments that aren't normally on Student Vue, being human error or some other reason, as you can now manually add your assignments. It allows you to mark assignments as complete, bringing them out of the to list, and will very soon get advanced functionality, such as scheduling days to work on certain assignments, which would show up when you request the list.
# How can I get assignment list?
**NOTE: Assignment list requires Python 3 to be installed**<br>
The installation process is simple (without Git method):
1. Download the [zip file](https://github.com/Whodiduexpect/assignment-list/archive/master.zip) (can also be accessed from GitHub page)
2. Extract the zip file to a folder on the computer
3. Open the terminal in that folder and get the dependencies:
<a/>
```
pip install -r requirements.txt
```
## How do I use assignment list?
The first time you use assignment list, it asks you for your Student Vue credentials. Here, we will just start it without asking it to do anything just to get it set up first.
```
python assignment-list.py
```
If everything is working, you should see it output:
```
First time setup - Please enter your student id number, your password and your district domain separated by commas.
```
Enter your student id number, your password, and your district domain (the first part of your login URL) separated by commas.
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
And the program would output it's help message.<br>
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
