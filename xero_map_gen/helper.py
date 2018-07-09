from copy import copy
import csv
import os

from traitlets import TraitError


class TraitValidation(object):
    @classmethod
    def path_exists(cls, path, name=None):
        if not os.path.exists(path):
            raise TraitError('%spath %s does not exist' % (
                (' %s' % name) if name else "",
                path
            ))

    @classmethod
    def not_none(cls, value, name=None):
        if value is None:
            raise TraitError('value %sis None' % (
                (" %s" % name) if name else "")
            )

    @classmethod
    def not_falsey(cls, value, name=None):
        if not value:
            raise TraitError('value %sis empty' % (
                (" %s" % name) if name else "")
            )

def semiflatten_api_contact(api_contact):
    semiflattened_contact = dict()
    for key in [
        'ContactID', 'ContactGroups', 'ContactNumber',
        'ContactStatus', 'EmailAddress', 'Name'
    ]:
        semiflattened_contact[key] = api_contact.get(key)
    for address in api_contact['Addresses']:
        address = copy(address)
        type = address.pop('AddressType', 'POBOX')
        key = '%s Address' % type
        assert key not in semiflattened_contact, "duplicate key being added"
        semiflattened_contact[key] = address
    for phone in api_contact['Phones']:
        phone = copy(phone)
        type = phone.pop('PhoneType', 'DEFAULT')
        key = '%s Phone' % type
        assert key not in semiflattened_contact, "duplicate key being added"
        semiflattened_contact[key] = phone
    return semiflattened_contact

def dump_api_contacts(api_contacts, dump_path='api_contacts.csv'):
    with open(dump_path, 'w') as dump_file:
        writer = csv.DictWriter(
            dump_file,
            {
                'ContactID': 'ContactID',
                'ContactGroups': 'ContactGroups',
                'ContactNumber': 'ContactNumber',
                'ContactStatus': 'ContactStatus',
                'EmailAddress': 'EmailAddress',
                'Name': 'Name',
                'POBOX Address': 'POBOX Address',
                'STREET Address': 'STREET Address',
                'DELIVERY Address': 'DELIVERY Address',
                'DEFAULT Phone': 'DEFAULT Phone',
                'DDI Phone': 'DDI Phone',
                'MOBILE Phone': 'MOBILE Phone',
                'FAX Phone': 'FAX Phone',
            },
            extrasaction='ignore'
        )
        writer.writeheader()
        for api_contact in api_contacts:
            semiflattened_contact = semiflatten_api_contact(api_contact)
            writer.writerow(semiflattened_contact)

def semiflatten_contact(contact):
    semiflattened_contact = semiflatten_api_contact(contact._data)
    for flat_key, attribute in [
        ('MAIN Address', 'main_address'),
        ('MAIN Phone', 'main_phone')
    ]:
        semiflattened_contact[flat_key] = getattr(contact, attribute)
    return semiflattened_contact

def dump_contacts(contacts, dump_path='contacts.csv'):
    with open(dump_path, 'w') as dump_file:
        writer = csv.DictWriter(
            dump_file,
            {
                'ContactID': 'ContactID',
                'ContactGroups': 'ContactGroups',
                'ContactNumber': 'ContactNumber',
                'ContactStatus': 'ContactStatus',
                'EmailAddress': 'EmailAddress',
                'Name': 'Name',
                'MAIN Address': 'MAIN Address',
                'POBOX Address': 'POBOX Address',
                'STREET Address': 'STREET Address',
                'DELIVERY Address': 'DELIVERY Address',
                'MAIN Phone': 'Main Phone',
                'DEFAULT Phone': 'DEFAULT Phone',
                'DDI Phone': 'DDI Phone',
                'MOBILE Phone': 'MOBILE Phone',
                'FAX Phone': 'FAX Phone',
            },
            extrasaction='ignore'
        )
        writer.writeheader()
        for contact in contacts:
            semiflattened_contact = semiflatten_contact(contact)
            writer.writerow(semiflattened_contact)
