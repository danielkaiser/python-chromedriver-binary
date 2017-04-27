from setuptools import setup
from setuptools.command.install import install
from chromedriver_binary import get_variable_separator, get_chromedriver_filename

import sys
import os
import zipfile
import shutil
import subprocess
try:
    from io import BytesIO
    from urllib.request import urlopen, URLError
except ImportError:
    from StringIO import StringIO as BytesIO
    from urllib2 import urlopen, URLError


def create_required_files():
    # License
    if not os.path.isfile('LICENSE.txt'):
        shutil.copyfile('LICENSE', 'LICENSE.txt')
    # Readme in reST format
    if not os.path.isfile('README.txt'):
        subprocess.call(['pandoc', 'README.md', '-t', 'rst', '-o', 'README.txt'])

create_required_files()
with open('README.txt') as file:
    long_description = file.read()


class DownloadChromedriver(install):
    @staticmethod
    def get_chromedriver_url(version='2.29'):
        base_url = 'https://chromedriver.storage.googleapis.com/'
        if sys.platform.startswith('linux'):
            platform = 'linux'
            architecture = '64' if sys.maxsize > 2 ** 32 else '32'
        elif sys.platform == 'darwin':
            platform = 'mac'
            architecture = '64'
        elif sys.platform.startswith('win'):
            platform = 'win'
            architecture = '32'
        else:
            raise RuntimeError('Could not determine chromedriver download URL for this platform.')
        return base_url + version + '/chromedriver_' + platform + architecture + '.zip'

    @staticmethod
    def find_binary_in_path(filename):
        if 'PATH' not in os.environ:
            return None
        for directory in os.environ['PATH'].split(get_variable_separator()):
            binary = os.path.join(directory, filename)
            if os.path.isfile(binary) and os.access(binary, os.X_OK):
                return binary
        return None

    def run(self):
        chromedriver_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chromedriver_binary')
        print(chromedriver_dir)
        chromedriver_filename = DownloadChromedriver.find_binary_in_path(get_chromedriver_filename())
        if chromedriver_filename:
            print("\nChromedriver already installed at {}...\n".format(chromedriver_filename))
            new_filename = os.path.join(chromedriver_dir, get_chromedriver_filename())
            self.copy_file(chromedriver_filename, new_filename)
        else:
            chromedriver_bin = get_chromedriver_filename()
            chromedriver_filename = os.path.join(chromedriver_dir, chromedriver_bin)
            if not os.path.isfile(chromedriver_filename):
                print("\nDownloading Chromedriver...\n")
                if not os.path.isdir(chromedriver_dir):
                    os.mkdir(chromedriver_dir)
                url = DownloadChromedriver.get_chromedriver_url()
                try:
                    response = urlopen(url)
                    if response.getcode() != 200:
                        raise URLError('Not Found')
                except URLError:
                    raise RuntimeError('Failed to download chromedriver archive: {}'.format(url))
                archive = BytesIO(response.read())
                with zipfile.ZipFile(archive) as zip_file:
                    zip_file.extract(chromedriver_bin, chromedriver_dir)
            else:
                print("\nChromedriver already installed at {}...\n".format(chromedriver_filename))
            if not os.access(chromedriver_filename, os.X_OK):
                os.chmod(chromedriver_filename, 0744)
        install.run(self)


setup(
    name="chromedriver-binary",
    version="2.29.0",
    author="Daniel Kaiser",
    author_email="daniel.kaiser94@gmail.com",
    description="A installer for chromedriver.",
    license="MIT",
    keywords="chromedriver chrome browser selenium splinter",
    url="https://github.com/danielkaiser/python-chromedriver-binary",
    packages=['chromedriver_binary'],
    package_data={
        'chromedriver_binary': ['chromedriver*']
    },
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={'install': DownloadChromedriver}
)