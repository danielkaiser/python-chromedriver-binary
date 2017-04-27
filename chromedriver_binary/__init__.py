import os
import sys


def get_chromedriver_filename():
    if sys.platform.startswith('win'):
        return 'chromedriver.exe'
    return 'chromedriver'


def get_variable_separator():
    if sys.platform.startswith('win'):
        return ';'
    return ':'


def add_chromedriver_to_path():
    chromedriver_dir = os.path.abspath(os.path.dirname(__file__))
    if 'PATH' not in os.environ:
        os.environ['PATH'] = chromedriver_dir
    elif chromedriver_dir not in os.environ['PATH']:
        os.environ['PATH'] += get_variable_separator()+chromedriver_dir


chromedriver_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), get_chromedriver_filename())
add_chromedriver_to_path()
