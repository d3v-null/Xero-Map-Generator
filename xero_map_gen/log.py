import os
import logging
import coloredlogs

from . import PKG_NAME

ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.setLevel(logging.DEBUG)
PKG_LOGGER = logging.getLogger(PKG_NAME)
PKG_STREAM_HANDLER = None
PKG_FILE_HANDLER = None

def setup_logging(stream_log_level=None, log_file=None, file_log_level=None):
    global PKG_FILE_HANDLER, PKG_STREAM_HANDLER

    if log_file:
        if PKG_FILE_HANDLER:
            PKG_LOGGER.removeHandler(PKG_FILE_HANDLER)
        PKG_FILE_HANDLER = logging.FileHandler(log_file)
        ROOT_LOGGER.addHandler(PKG_FILE_HANDLER)
    if file_log_level:
        PKG_FILE_HANDLER.setLevel(file_log_level)
    if stream_log_level:
        if not PKG_STREAM_HANDLER:
            PKG_STREAM_HANDLER = logging.StreamHandler()
            if os.name != 'nt':
                PKG_STREAM_HANDLER.setFormatter(coloredlogs.ColoredFormatter())
            PKG_STREAM_HANDLER.addFilter(coloredlogs.HostNameFilter())
            PKG_STREAM_HANDLER.addFilter(coloredlogs.ProgramNameFilter())
            ROOT_LOGGER.addHandler(PKG_STREAM_HANDLER)
        PKG_STREAM_HANDLER.setLevel(stream_log_level)

    # TODO: maybe process quiet differently so that it does not add a stream handler
    if PKG_STREAM_HANDLER:
        logging.info("stream log level: %s", PKG_STREAM_HANDLER.level)
    if PKG_FILE_HANDLER:
        logging.info("file log level: %s", PKG_FILE_HANDLER.level)

setup_logging()
