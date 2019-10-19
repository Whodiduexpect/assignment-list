from setuptools import setup

setup(
    name='assignmentlist',
    version='v1.0.3-beta',
    packages=['assignmentlist'],
    url='https://github.com/Whodiduexpect/assignment-list',
    license='MIT',
    author='Whodiduexpect',
    description='A Student Vue assignment manager',
    python_requires='>=3.6',
    install_requires=[
        "studentvue",
        "pandas",
        "click",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        assignmentlist=assignmentlist.assignmentlist:cli
    ''',
)
