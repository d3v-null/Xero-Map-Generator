"""
Test container functionality.
"""

import datetime
import unittest

import pytest

from .test_core import AbstractXMGTestCase
from ..contain import XeroContact


class ContainTestCase(AbstractXMGTestCase):
    pass


class XeroContactTestCase(ContainTestCase):
    # def setUp(self):
    #     super().setUp()

    # Data generated with https://mockaroo.com/4d8d5630

    def test_contact_basic(self):
        api_data = {
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
                           'Country': '',
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

        sanitized_data = {
            "Company Name": "Eare Pharmacy",
            "Address": "9571 Mariners Cove Place",
            "Area": "Sydney",
            "Postcode": "1033",
            "State": "NSW",
            "Country": "Australia",
            "Phone": "68891038",
        }

        contact = XeroContact(api_data)

        self.assertEqual(contact.company_name, sanitized_data['Company Name'])
        self.assertEqual(contact.main_address, api_data['Addresses'][1])
        self.assertEqual(contact.first_main_address_line, sanitized_data['Address'])
