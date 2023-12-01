import logging
import os
from sys import stdout

_name_to_level = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}

logger = logging.getLogger()
logger.propagate = False

console_handler = logging.StreamHandler(stream=stdout)
console_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

log_level = _name_to_level.get(os.environ.get('log_level'), logging.WARNING)
logger.setLevel(log_level)
logging.captureWarnings(True)


def get_logger(log_name, level=None):
    module_logger = logging.getLogger(log_name)
    if level is not None:
        module_logger.setLevel(level)
    return module_logger
