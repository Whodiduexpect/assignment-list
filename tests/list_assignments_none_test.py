import sys
from io import StringIO

import pandas as pd

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
    assignments = pd.DataFrame({'Assignment ID': [], 'Class Name': [], 'Due Date': [
    ], 'Assignment': [], 'is_completed': []})
    with Capturing() as output:
        assignment_list.list_assignments(assignments)
    assert output == ['No assignments to do!']
