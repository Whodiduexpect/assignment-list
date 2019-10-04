import pytest
import subprocess
import sys
sys.path.append("")
import assignment_list


def test_answer():
    assignment_list.createIfNotExist("studentvue_credentials")
    result = subprocess.run(['python3', 'assignment_list.py'], stdout=subprocess.PIPE)
    assert "Usage:" in result.stdout.decode("utf-8")
