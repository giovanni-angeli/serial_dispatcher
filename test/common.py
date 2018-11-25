# coding: utf-8

from os import path

import serial_dispatcher

here = path.abspath(path.dirname(__file__))
with open(path.join(here, '../serial_dispatcher', '__version__'), encoding='utf-8') as f:
    expected__version__ = f.read().strip()


def check_version():

    assert (expected__version__ == serial_dispatcher.__version__)

