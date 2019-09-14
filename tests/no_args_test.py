import sys
from io import StringIO
from pathlib import Path
import pytest
import os
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
    if not os.path.exists("data"):
        os.mkdir("data")
    assignment_list.create_if_not_exist("credentials")
    with Capturing() as output:
        assignment_list.start()
    assert output == [
        "Did you mean to do something? Try adding the argument \"--help\""]
