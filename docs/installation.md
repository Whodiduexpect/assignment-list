# Installing Assignment List

## Prerequisites

Assignment List requires [Python](https://www.python.org/downloads/) 3.6 or later (make sure you install pip with your installation)

## Installing

1. Download the [zip file](https://github.com/Whodiduexpect/assignment-list/archive/master.zip)
2. Extract it to where you want Assignment List to be
3. Open the terminal in the folder you extracted
4. Get the dependencies:
	```
	pip3 install -r requirements.txt
	```

And now to test it:
```
python assignment_list.py
```
It should then prompt you with the initial setup. From there you can try listing the current assignments:

```
python assignment_list.py list
```

```
                                        Assignment  Assignment ID                  Class Name    Due Date
0                               Test Assignment #1        1111111     Last, F  TESTCLASS I(1)   1/01/2019
1                               Test Assignment #2        2222222    Last, F  TESTCLASS II(2)   1/01/2019
2                               Test Assignment #3        3333333   Last, F  TESTCLASS III(3)   1/01/2019
```
For full usage instructions, [read the usage instructions](usage.md).

	Note:
	If you have issues with pip3 not being found, try using pip instead of pip3
	If you have issues with the command python, try using python3 instead.
[Go back](https://assignment-list.computer)
