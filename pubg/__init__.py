# -*- coding: utf-8 -*-

"""

An asyncio friendly wrapper for the Riot's League API.

:copyright: (c) 2017-2018 Datmellow
:license: MIT, see LICENSE for more details.

"""
import logging
from collections import namedtuple

__title__ = "pubg"
__author__ = "Datmellow"
__license__ = "MIT"
__copyright__ = "Copyright 2017-2018 Datmellow"
__version__ = "0.0.1a"

from pubg.client import PubGClient

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=0, micro=1, releaselevel='alpha', serial=0)

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
