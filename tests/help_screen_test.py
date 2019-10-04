import pytest
import subprocess


def test_answer():
    result = subprocess.run(['python3', 'assignment_list.py'], stdout=subprocess.PIPE)
    assert "Usage:" in result.stdout.decode("utf-8")
