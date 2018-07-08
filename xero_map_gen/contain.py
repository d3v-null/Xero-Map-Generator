""" Container classes and utilities for containing data. """

class XeroContactGroup(object):
    pass

class XeroContact(object):
    def __init__(self, data):
        self._data = data


        if 'Addresses' in data and data.get('Addresses') :
            addresses = data['Addresses']
            main_address = None
            for address in addresses:
                nonempty_address_lines = {}
                for addressline in range(1, 5):
                    key = 'AddressLine%d' % addressline
                    if key in address and address[key]:
                        nonempty_address_lines[key] = address[key]
                if not nonempty_address_lines:
                    continue

    @property
    def company_name(self):
        if 'Name' in self._data and self._data.get('Name') :
            return self._data['Name']


    def to_dict(self):
        response = {}
        for key, value in dir(self):
            if key.startswith('_'):
                continue
            response[key] = value
