import studentvue_parser
import sys
from io import StringIO
import pytest


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def test_answer(capsys):
    with pytest.raises(ValueError):
        studentvue_parser.authenticate(["3123", "pass", "w"])
