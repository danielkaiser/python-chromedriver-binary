# coding: utf-8
"""
This will add the executable to your PATH so it will be found.
The filename of the binary is stored in `chromedriver_filename`.
"""

import os
from . import utils


def add_chromedriver_to_path():
    """
    Appends the directory of the chromedriver binary file to PATH.
    """
    chromedriver_dir = os.path.abspath(os.path.dirname(__file__))
    if 'PATH' not in os.environ:
        os.environ['PATH'] = chromedriver_dir
    elif chromedriver_dir not in os.environ['PATH']:
        os.environ['PATH'] = chromedriver_dir + utils.get_variable_separator() + os.environ['PATH']


chromedriver_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), utils.get_chromedriver_filename())
add_chromedriver_to_path()
