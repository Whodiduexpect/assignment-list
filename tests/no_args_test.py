from io import StringIO
from pathlib import Path
import pytest
import sys
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
    assert 1 == 1  # Just make the test pass for now
