# -*- coding: utf-8 -*-

import os
from codecs import open
here = os.path.abspath(os.path.dirname(__file__))
__version__ = None
with open(os.path.join(here, '__version__'), encoding='utf-8') as f:
    __version__ = f.read().strip()

