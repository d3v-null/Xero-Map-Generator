"""
Test transport functionality.
"""

import unittest

import pytest
from six import MovedModule, add_move

from ..transport import XeroApiWrapper
from .test_core import AbstractXMGTestCase

if True:
    add_move(MovedModule('mock', 'mock', 'unittest.mock'))
    from six.moves import mock

    from mock import patch

class TransportTestCase(AbstractXMGTestCase):
    def test_transport_basic(self):
        with \
            patch.object(XeroApiWrapper, '__init__', return_value=None)\
        :
            xero = XeroApiWrapper()
