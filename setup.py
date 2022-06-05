from setuptools import setup, find_packages
from setuptools.command.test import test as test_command
import sys
import os

PACKAGE_NAME = 'bingo_simulator'
VERSION_FILENAME = 'version.py'
DESCRIPTION = '"Bingo Simulator that plots histograms of the results."'
AUTHOR = 'Colin Huber'
AUTHOR_EMAIL = 'cbhuber@gmail.com'
INSTALL_REQUIRES = ['']


'''AUTOMATICALLY GENERATED. DO NOT MODIFY ANYTHING BELOW THIS UNLESS YOU KNOW WHAT YOU ARE DOING'''

VERSION_PATH = os.path.join(os.path.dirname(__file__), PACKAGE_NAME, VERSION_FILENAME)

main_ns = {}
with open(VERSION_PATH) as ver_file:
    exec(ver_file.read(), main_ns)
VERSION = main_ns['__version__']


class PyTestCommand(test_command):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        test_command.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        import pytest
        print(self.pytest_args)
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(exclude=['test', 'doc']),
    cmdclass={'test': PyTestCommand},
    tests_require=['pytest'],
    install_requires=INSTALL_REQUIRES,
    entry_points={},
    include_package_data=True,
    zip_safe=False,)
