import os
import unittest

import pytest

from . import TESTS_DATA_DIR
from ..config import load_config, load_cli_config, load_file_config
from ..log import setup_logging, PKG_LOGGER


@pytest.mark.usefixtures("debug")
class AbstractXMGTestCase(unittest.TestCase):
    config_file = "config.json"
    config_dir = TESTS_DATA_DIR
    override_args = ''
    debug = False

    def setUp(self):
        cli_config = load_cli_config(self.override_args.split(), has_extra_config=True)
        config_files = []
        if self.config_file:
            self.config_file
            config_files.append(self.config_file)
        if cli_config.BaseConfig.config_file:
            config_files.append(cli_config.BaseConfig.config_file)
        self.conf = load_file_config(config_files, self.config_dir)
        self.conf.merge(cli_config)

        if self.debug:
            self.conf.LogConfig.stream_log_level = "DEBUG"
        else:
            self.conf.LogConfig.stream_log_level = "WARNING"

        setup_logging(**dict(self.conf.LogConfig))

        PKG_LOGGER.debug("Completed setUp of class %s", self.__class__.__name__)
