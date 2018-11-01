"""
Test transport functionality.
"""

import unittest

import pytest
from six import MovedModule, add_move

from xero_map_gen.transport import XeroApiWrapper
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

    def test_get_contacts_by_ids(self):
        with \
            patch.object(XeroApiWrapper, '__init__', return_value=None),\
            patch.object(
                XeroApiWrapper,
                'rate_limit_retry_query',
                return_value=[self.example_api_contact]
            )\
        :
            xero = XeroApiWrapper()
            contacts = xero.get_contacts_by_ids(['fake_id'], limit=1)

        self.assertEqual(len(contacts), 1)
