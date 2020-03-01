![Tests](https://github.com/Whodiduexpect/assignment-list/workflows/Tests/badge.svg)
# Assignment List

Assignment list is a terminal-based assignment manager for the Student Vue web portal. Assignment List is meant to replace the lack of features in Student Vue by giving tools to manage assignments, like a fancy integrated to-do list. If you just want a CLI Student Vue interface, [check out this neat project.](https://github.com/kajchang/studentvue-cli)

## Getting Started

These instructions will get you a copy of Assignment List up and running on your machine.

### Prerequisites

Assignment List works with Python 3.6 or later

### Installing

Clone the repository (with Git)

```
git clone https://github.com/Whodiduexpect/assignment-list.git
```

Change directory and install the dependencies

```
cd assignment-list
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
For full usage instructions, see [USAGE.md](USAGE.md)

## Running the tests
Assignment List has rather primitive tests that you can run with pytest.
```
pip3 install pytest
```
```
pytest
```
### What do the tests do?
There are currently 5 basic tests:
* `help_screen_test.py`, which tests that the click help screen appears when no arguments are called
* `invalid_credentials_test.py`, which tests that Assignment List correctly handles situations where the Student Vue credentials are incorrect
* `list_assignments_none_test.py`, which tests that Assignment List correctly reports that there are no current assignments
* `list_completed_none_test.py`, which tests that Assignment List correctly reports that there are no completed assignments
* `list_added_none_test.py`, which tests that Assignment List correctly reports that there are no added assignments

These tests are mainly to make sure that Assignment List isn't completely broken, and don't test the core functionality of Assignment List.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [releases on this repository](https://github.com/Whodiduexpect/assignment-list/releases). 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [Student Vue API, Unofficial Python API for StudentVue Portals](https://github.com/kajchang/StudentVue)
