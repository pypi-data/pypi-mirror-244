import os
from setuptools import setup
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import versioneer

if __name__ == "__main__":
    setup(name='netneurotools-scipyfix',
          version="0.0.0",
          )
