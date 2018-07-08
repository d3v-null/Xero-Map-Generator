import os
import unittest

import pytest

from . import TESTS_DATA_DIR
from ..config import load_config
from ..log import setup_logging, PKG_LOGGER


@pytest.mark.usefixtures("debug")
class AbstractXMGTestCase(unittest.TestCase):
    config_file = os.path.join(TESTS_DATA_DIR, "config.json")
    override_args = ''
    debug = False

    def setUp(self):
        self.conf = load_config(
            argv=self.override_args.split(),
            extra_config_files=[self.config_file]
        )

        if self.debug:
            self.conf.LogConfig.stream_log_level = "DEBUG"
        else:
            self.conf.LogConfig.stream_log_level = "WARNING"

        setup_logging(**dict(self.conf.LogConfig))

        PKG_LOGGER.debug("Completed setUp of class %s", self.__class__.__name__)
