# chromedriver-binary
Downloads and installs the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) binary version 2.43 for automated testing of webapps. The installer supports Linux, MacOS and Windows operating systems.

## Installation

### From PyPI
```
pip install chromedriver-binary
```

### From GitHub
```
pip install git+https://github.com/danielkaiser/python-chromedriver-binary.git
```

## Usage
To use chromedriver just `import chromedriver_binary`. This will add the executable to your PATH so it will be found. You can also get the absolute filename of the binary with `chromedriver_binary.chromedriver_filename`.

### Example
```
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
```

### Exporting chromedriver binary path
This package installs a small shell script `chromedriver-path` to easily set and export the PATH variable:
```
$ export PATH=$PATH:`chromedriver-path`
```
