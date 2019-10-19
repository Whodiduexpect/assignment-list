import os
import subprocess
import sys

sys.path.append("")
import assignment_list


def test_answer():
    if not os.path.exists("data"):
        os.mkdir("data")
    assignment_list.create_if_not_exist("studentvue_credentials")
    result = subprocess.run(
        ['python3', 'assignment_list.py'], stdout=subprocess.PIPE)
    assert "Usage:" in result.stdout.decode("utf-8")
