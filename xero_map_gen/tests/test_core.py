import datetime
import os
import shlex
import unittest

import pytest
from traitlets.config.loader import Config

from . import TESTS_DATA_DIR
from ..config import load_cli_config, load_config, load_file_config
from ..contain import XeroContact
from ..log import PKG_LOGGER, setup_logging


@pytest.mark.usefixtures("debug")
class AbstractXMGTestCase(unittest.TestCase):
    config_dir = TESTS_DATA_DIR
    config_path = "config.json"
    override_args = ''
    debug = False

    example_api_contact = {
        'Addresses': [{'AddressType': 'STREET',
                       'AttentionTo': '',
                       'City': '',
                       'Country': '',
                       'PostalCode': '',
                       'Region': ''},
                      {'AddressLine1': '9571 Mariners Cove Place',
                       'AddressLine2': '',
                       'AddressLine3': '',
                       'AddressLine4': '',
                       'AddressType': 'POBOX',
                       'AttentionTo': 'John Smith',
                       'City': 'Sydney',
                       'Country': 'AU',
                       'PostalCode': '1033',
                       'Region': 'NSW'}],
        'Attachments': [],
        'BankAccountDetails': '',
        'ContactGroups': [{'ContactGroupID': '4f935b4a-9406-41c0-ba45-b36b67c0123e',
                           'Contacts': [],
                           'HasValidationErrors': False,
                           'Name': 'ACME Agencies',
                           'Status': 'ACTIVE'}],
        'ContactID': 'a3e4631c-c02d-461d-a5ec-641c5aaace1f',
        'ContactNumber': '',
        'ContactPersons': [],
        'ContactStatus': 'ACTIVE',
        'DefaultCurrency': 'AUD',
        'EmailAddress': 'grohlfing0@reddit.com',
        'FirstName': 'John',
        'HasAttachments': False,
        'HasValidationErrors': False,
        'IsCustomer': True,
        'IsSupplier': False,
        'LastName': 'Smith',
        'Name': 'Eare Pharmacy',
        'PaymentTerms': {'Sales': {'Day': 30, 'Type': 'DAYSAFTERBILLDATE'}},
        'Phones': [{'PhoneAreaCode': '',
                    'PhoneCountryCode': '',
                    'PhoneNumber': '',
                    'PhoneType': 'DDI'},
                   {'PhoneAreaCode': '02',
                    'PhoneCountryCode': '',
                    'PhoneNumber': '68891038',
                    'PhoneType': 'DEFAULT'},
                   {'PhoneAreaCode': '02',
                    'PhoneCountryCode': '',
                    'PhoneNumber': '68892299',
                    'PhoneType': 'FAX'},
                   {'PhoneAreaCode': '',
                    'PhoneCountryCode': '',
                    'PhoneNumber': '',
                    'PhoneType': 'MOBILE'}],
        'TaxNumber': '27 604 367 587',
        'UpdatedDateUTC': datetime.datetime(2017, 2, 20, 18, 14, 30, 327000)
    }

    def setUp(self):
        config_paths = []
        if self.config_path:
            config_paths.append(self.config_path)
        proto_conf = Config()
        proto_conf.LogConfig = Config()
        if self.debug:
            proto_conf.LogConfig.stream_log_level = "DEBUG"
        else:
            proto_conf.LogConfig.stream_log_level = "WARNING"
        proto_conf.BaseConfig = Config()
        proto_conf.BaseConfig.config_dir = self.config_dir
        proto_conf.BaseConfig.config_path = self.config_path

        self.conf = load_config(
            shlex.split(self.override_args),
            proto_conf
        )

        setup_logging(**dict(self.conf.LogConfig))

        PKG_LOGGER.debug("Completed setUp of class %s", self.__class__.__name__)

class XMGCoreTestCase(AbstractXMGTestCase):
    def test_get_map_contacts(self):
        pass

    def test_dump_map_contacts(self):
        map_contacts = [
            XeroContact(self.example_api_contact)
        ]
