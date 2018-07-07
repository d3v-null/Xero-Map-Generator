import os
from traitlets import TraitError
import csv

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


def dump_api_contacts(api_contacts, dump_path='contacts.csv'):
    with open(dump_path, 'w') as dump_file:
        writer = csv.DictWriter(
            dump_file,
            {
                'ContactID': 'ContactID',
                'Addresses': 'Addresses',
                'ContactGroups': 'ContactGroups',
                'ContactNumber': 'ContactNumber',
                'ContactStatus': 'ContactStatus',
                'EmailAddress': 'EmailAddress',
                'Name': 'Name',
                'Phones': 'Phones',
            },
            extrasaction='ignore'
        )
        writer.writeheader()
        for api_contact in api_contacts:
            writer.writerows(api_contact)
