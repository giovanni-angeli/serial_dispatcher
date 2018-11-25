# -*- coding: utf-8 -*-


"""A setuptools based setup module for pip usage.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from codecs import open
from os import (path, linesep)
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.readlines()

with open(path.join(here, 'serial_dispatcher', '__version__'), encoding='utf-8') as f:
    __version__ = f.read().strip()

SETUP_KW_ARGS = {
    'name': 'serial_dispatcher',
    'version': __version__,
    'description': long_description[0],
    'long_description': linesep.join(long_description),
    'url': 'https://github.com/giovanni-angeli/serial_dispatcher',
    'author': 'giovanni angeli',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    'install_requires': [
        "pyserial",  # ==3.4
        "pyserial-asyncio",  # ==2.10.6
        "pytest",  # ==2.10.6
    ],
    'package_data': {
        'serial_dispatcher': [
            '__version__',
        ]
    },
    'entry_points': {
        'console_scripts': [
            'serial_dispatcher=serial_dispatcher:main',
        ],
    },
    'packages': find_packages(exclude=['docs', 'tmp', 'log', 'venv', 'dist_dir'])
}

if __name__ == "__main__":
    setup(**SETUP_KW_ARGS)
