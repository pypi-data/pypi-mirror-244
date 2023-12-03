# Python Library Starter

This is a simple example of a Python library.

## Commands
venv:
```
python3 -m venv venv
source venv/bin/activate
pip install wheel setuptools twine pytest-runner==4.4 pytest==4.4.1
```

test:
```
python setup.py pytest
```

build:
```
python setup.py bdist_wheel
```

install:
```
pip install dist/wheelfile.whl
```

import:
```
import mypythonlib
from mypythonlib import myfunctions
```
