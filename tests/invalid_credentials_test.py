import pytest
import subprocess
import sys
import os
sys.path.append('')
import assignment_list


def test_answer():
    if not os.path.exists('data'):
        os.mkdir('data')
    file = assignment_list.openData('studentvue_credentials', 'r')
    contents = file.read()
    file.close()
    file = assignment_list.openData('studentvue_credentials', 'w+')
    file.close()
    result = subprocess.run(
        ['python3', 'assignment_list.py', 'list'], stdout=subprocess.PIPE)
    file = assignment_list.openData('studentvue_credentials', 'w+')
    file.write(contents)
    file.close()
    assert "python assignment_list.py reset" in result.stdout.decode("utf-8")
