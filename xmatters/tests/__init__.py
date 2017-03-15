import logging
import os
import tempfile

_log_dir = tempfile.gettempdir()
_log_dir = '/tmp'
_log_filename = _log_dir + os.sep + 'xlogger.log'
_log_level = logging.DEBUG