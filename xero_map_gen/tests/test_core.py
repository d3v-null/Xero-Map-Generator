import os
import shlex
import unittest

import pytest

from . import TESTS_DATA_DIR
from ..config import load_cli_config, load_config, load_file_config
from ..log import PKG_LOGGER, setup_logging


@pytest.mark.usefixtures("debug")
class AbstractXMGTestCase(unittest.TestCase):
    config_file = "config.json"
    config_dir = TESTS_DATA_DIR
    override_args = ''
    debug = False

    def setUp(self):
        config_files = []
        if self.config_file:
            config_files.append(self.config_file)
        self.conf = load_config(
            shlex.split(self.override_args),
            extra_config_files=config_files,
            config_path=self.config_dir
        )

        if self.debug:
            self.conf.LogConfig.stream_log_level = "DEBUG"
        else:
            self.conf.LogConfig.stream_log_level = "WARNING"

        setup_logging(**dict(self.conf.LogConfig))

        PKG_LOGGER.debug("Completed setUp of class %s", self.__class__.__name__)

class XMGCoreTestCase(AbstractXMGTestCase):
    def test_main(self):
        pass
