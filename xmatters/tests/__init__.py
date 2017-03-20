"""Variables used by the test modules
"""
import logging
import os
import tempfile

_LOG_DIR = tempfile.gettempdir()
_LOG_DIR = '/tmp'
_LOG_FILENAME = _LOG_DIR + os.sep + 'xlogger.log'
_LOG_LEVEL = logging.DEBUG
