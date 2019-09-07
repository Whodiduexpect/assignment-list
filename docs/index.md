# What is assignment list?
## Why was it created?
Assignment list was created because of districts that put all their assignments in a Student Vue web portal. If you don't know Student Vue, this might sound great as it puts all the assignments in one place. 
## Why Student Vue is unfit for assignments
However, Student Vue is poorly designed when it comes to assignments. The only thing it has to offer is a simple calendar with the name of the assignment. That's it - there are no organization tools, you just have to remember which ones you have done, and you can't manually add anything. You can't even filter any assignments, so every time you want to take a look you have to look at every assignment that month. And if it's the last day of the month you have to go all the way to next month just for one day.
## What does assignment list do to help?
It's easy, **all** your assignments are in one quick to access place. This includes assignments that aren't normally on Student Vue, being human error or some other reason, as you can now manually add your assignments. It allows you to mark assignments as complete, bringing them out of the to list, and will very soon get advanced functionality, such as scheduling days to work on certain assignments, which would show up when you request the list.
# How can I get assignment list?
## I know how all of this works
Great, check out the [README](https://github.com/Whodiduexpect/assignment-list/blob/master/README.md) on GitHub.
## I don't really know what I'm doing
The first thing you'll need is Python 3. Specificaly, that's Python 3.6 and later. Downloads of Python can be found on the [Python download page](https://www.python.org/downloads/)<br>
Once you have Python installed the installation is simple:
1. Download the [zip file](https://github.com/Whodiduexpect/assignment-list/archive/master.zip)
2. Extract the zip file to a folder on the computer
3. Open the terminal in that folder and get the dependencies:
```
pip install -r requirements.txt
```
If you have issues with the command above, you can also try:
```
pip3 install -r requirements.txt
```

### I feel like you're going a bit too fast for my liking...
Well, if you're still confused, you click on the [zip file](https://github.com/Whodiduexpect/assignment-list/archive/master.zip) (the link), you select a folder where to put it, you accept it and you let it download. Then, you should be able to open the folder where you put the zip file, right click it and select an option that's along the lines of "extract". From there you should be able to extract the zip file somewhere and open the terminal in the folder (do a web search on how you do this on your operating system if you need to) and you enter the following into the terminal:
```
pip install -r requirements.txt
```
and if it gave an error, try
```
pip3 install -r requirements.txt
```

# How do I use assignment list?
The first time you use assignment list, it asks you for your Student Vue credentials. Here, we will just start it without asking it to do anything just to get it set up first.
```
python assignment_list.py
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
For this demonstration, let's follow through with that suggestion:
```
python assignment_list.py --help
```
```
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
```
Now, let's break it down:
* There are five commands
    - "--help" or "-h" which shows this help screen
    - "--complete" or "-c" which completes an assignment
    - "--add" or "-a" which adds an assignment that is not present in Student Vue
    - "--incomplete" or "-i" which marks a complete assignment as incomplete
    - "--list" or "-l" which shows you the assignment list
#### Testing it out
Now let's test out these features.
First off, we check the assignments we have due:
```
python assignment_list.py --list
```
```
-- Assignment List --
1. Test assignment
2. Algebra assignment from Student Vue
```
Now that we have the list, we will mark the second one as complete:
```
python assignment_list.py --complete 2
```
```
Marked assignment #2 as complete
```
We then check the list again
```
python assignment_list.py -l
```
```
-- Assignment List --
1. Test assignment
```
It's gone! Let's try adding an assignment manually
```
python assignment_list.py --add "Some assignment that was not added"
```
```
Added assignment "Some assignment that was not added"
```
To make sure that what we did worked, let's check the list once again
```
python assignment_list.py --list
```
```
-- Assignment List --
1. Some assignment that was not added
2. Test assignment
```
Whoops! Turns out that algerbra worksheet had a backside... Let's fix that
```
python assignment_list.py --incomplete "Algebra assignment from Student Vue"
```
```
Marked assignment "Algebra assignment from Student Vue" as incomplete
```
And if we pull up the list:
```
python assignment_list.py -l
```
```
-- Assignment List --
1. Some assignment that was not added
2. Algebra assignment from Student Vue
3. Test assignment
```
