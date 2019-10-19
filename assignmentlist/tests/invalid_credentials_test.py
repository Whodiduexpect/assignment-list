import os
import subprocess
import sys

sys.path.append('')
import assignment_list


def test_answer():
    if not os.path.exists('data'):
        os.mkdir('data')
    file = assignment_list.open_data('studentvue_credentials', 'r')
    contents = file.read()
    file.close()
    file = assignment_list.open_data('studentvue_credentials', 'w+')
    file.close()
    result = subprocess.run(
        ['python3', 'assignment_list.py', 'list'], stdout=subprocess.PIPE)
    file = assignment_list.open_data('studentvue_credentials', 'w+')
    file.write(contents)
    file.close()
    assert "python assignment_list.py reset" in result.stdout.decode("utf-8")
