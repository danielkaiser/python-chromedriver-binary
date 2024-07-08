from setuptools import setup
from setuptools.command.build_py import build_py
from chromedriver_binary.utils import get_chromedriver_filename, get_chromedriver_url, find_binary_in_path, check_version

import os
import ssl
import zipfile

try:
    from io import BytesIO
    from urllib.request import urlopen, URLError
    ssl_context = ssl.create_default_context()
except ImportError:
    from StringIO import StringIO as BytesIO
    from urllib2 import urlopen, URLError
    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)

__author__ = 'Daniel Kaiser <d.kasier@fz-juelich.de>'


with open('README.md') as readme_file:
    long_description = readme_file.read()


class DownloadChromedriver(build_py):
    def run(self):
        """
        Downloads, unzips and installs chromedriver.
        If a chromedriver binary is found in PATH it will be copied, otherwise downloaded.
        """
        chromedriver_version='128.0.6582.0'
        chromedriver_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chromedriver_binary')
        chromedriver_filename = find_binary_in_path(get_chromedriver_filename())
        if chromedriver_filename and check_version(chromedriver_filename, chromedriver_version):
            print("\nChromedriver already installed at {}...\n".format(chromedriver_filename))
            new_filename = os.path.join(chromedriver_dir, get_chromedriver_filename())
            self.copy_file(chromedriver_filename, new_filename)
        else:
            chromedriver_bin = get_chromedriver_filename()
            chromedriver_filename = os.path.join(chromedriver_dir, chromedriver_bin)
            if not os.path.isfile(chromedriver_filename) or not check_version(chromedriver_filename, chromedriver_version):
                print("\nDownloading Chromedriver...\n")
                if not os.path.isdir(chromedriver_dir):
                    os.mkdir(chromedriver_dir)
                url = get_chromedriver_url(version=chromedriver_version)
                try:
                    response = urlopen(url, context=ssl_context)
                    if response.getcode() != 200:
                        raise URLError('Not Found')
                except URLError:
                    raise RuntimeError('Failed to download chromedriver archive: {}'.format(url))
                archive = BytesIO(response.read())
                with zipfile.ZipFile(archive) as zip_file:
                    for filename in zip_file.namelist():
                        zip_file.extract(filename, chromedriver_dir)
                        path_elements = os.path.split(filename)
                        if len(path_elements) > 1:
                            os.rename(os.path.join(chromedriver_dir, filename), os.path.join(chromedriver_dir, path_elements[-1]))
            else:
                print("\nChromedriver already installed at {}...\n".format(chromedriver_filename))
            if not os.access(chromedriver_filename, os.X_OK):
                os.chmod(chromedriver_filename, 0o744)
        build_py.run(self)


setup(
    name="chromedriver-binary",
    version="128.0.6582.0.0",
    author="Daniel Kaiser",
    author_email="daniel.kaiser94@gmail.com",
    description="Installer for chromedriver.",
    license="MIT",
    keywords="chromedriver chrome browser selenium splinter",
    url="https://github.com/danielkaiser/python-chromedriver-binary",
    packages=['chromedriver_binary'],
    package_data={
        'chromedriver_binary': ['chromedriver*']
    },
    entry_points={
        'console_scripts': ['chromedriver-path=chromedriver_binary.utils:print_chromedriver_path'],
    },
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Installation/Setup",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={'build_py': DownloadChromedriver}
)
