""" Container classes and utilities for containing data. """

class XeroContactGroup(object):
    pass

class XeroContact(object):
    def __init__(self, data):
        self._data = data

    @property
    def main_address(self):
        if getattr(self, '_main_address', None):
            return self._main_address
        if 'Addresses' in self._data and self._data.get('Addresses') :
            addresses = self._data['Addresses']
            for address in addresses:
                if any([
                    value for key, value in address.items() \
                    if key.startswith("AddressLine")
                ]):
                    self._main_address = address
                    return self._main_address

    @property
    def company_name(self):
        if 'Name' in self._data and self._data.get('Name') :
            return self._data['Name']

    @property
    def first_main_address_line(self):
        main_address = self.main_address
        for line in range(1, 5):
            key = "AddressLine%d" % line
            if key in self.main_address and self.main_address[key]:
                return self.main_address[key]


    def to_dict(self):
        response = {}
        for key, value in dir(self):
            if key.startswith('_'):
                continue
            response[key] = value
