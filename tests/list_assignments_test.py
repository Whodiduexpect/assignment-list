from io import StringIO
from pathlib import Path
import pytest
import sys
sys.path.append('../')
sys.path.append("")
import assignment_list
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
def test_answer():
    with Capturing() as output:
        assignment_list.list_assignments(["Test Assignment 1", "test assignment 2", 28])
    assert output == ['-- Assignment List --', '1. Test Assignment 1', '2. test assignment 2', '3. 28']

    with Capturing() as output:
        assignment_list.list_assignments([])
    assert output == ['No assignments to do!']