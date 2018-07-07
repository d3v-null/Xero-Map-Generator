""" Container classes and utilities for containing data. """

class XeroContactGroup(object):
    pass

class XeroContact(object):
    def __init__(self, data):
        self._data = data
        if 'Name' in data and data.get('Name') :
            self.company_name = data['Name']

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


    def to_dict(self):
        response = {}
        for key, value in dir(self):
            if key.startswith('_'):
                continue
            response[key] = value

"""
EXAMPLE:
-------

Convert this
```python
  'Addresses': [{'AddressType': 'STREET',
                 'AttentionTo': '',
                 'City': '',
                 'Country': '',
                 'PostalCode': '',
                 'Region': ''},
                {'AddressLine1': '53 Dandalloo Street',
                 'AddressLine2': '',
                 'AddressLine3': '',
                 'AddressLine4': '',
                 'AddressType': 'POBOX',
                 'AttentionTo': 'Sally Sheehan',
                 'City': 'NARROMINE',
                 'Country': '',
                 'PostalCode': '2830',
                 'Region': 'NSW'}],
  'Attachments': [],
  'BankAccountDetails': '',
  'ContactGroups': [{'ContactGroupID': 'fbcf7743-e5da-4f0e-8bbd-125073a4e051',
                     'Contacts': [],
                     'HasValidationErrors': False,
                     'Name': 'Gordon Cohen Agencies',
                     'Status': 'ACTIVE'}],
  'ContactID': 'a3e4631c-c02d-461d-a5ec-641c5aaace1f',
  'ContactNumber': '',
  'ContactPersons': [],
  'ContactStatus': 'ACTIVE',
  'DefaultCurrency': 'AUD',
  'EmailAddress': 'narromine@lawlerspharmacy.com.au',
  'FirstName': 'Sally',
  'HasAttachments': False,
  'HasValidationErrors': False,
  'IsCustomer': True,
  'IsSupplier': False,
  'LastName': 'Sheehan',
  'Name': 'NARROMINE Pharmacy',
  'PaymentTerms': {'Sales': {'Day': 30, 'Type': 'DAYSAFTERBILLDATE'}},
  'Phones': [{'PhoneAreaCode': '',
              'PhoneCountryCode': '',
              'PhoneNumber': '',
              'PhoneType': 'DDI'},
             {'PhoneAreaCode': '02',
              'PhoneCountryCode': '',
              'PhoneNumber': '68891039',
              'PhoneType': 'DEFAULT'},
             {'PhoneAreaCode': '02',
              'PhoneCountryCode': '',
              'PhoneNumber': '68892295',
              'PhoneType': 'FAX'},
             {'PhoneAreaCode': '',
              'PhoneCountryCode': '',
              'PhoneNumber': '',
              'PhoneType': 'MOBILE'}],
  'TaxNumber': '27 604 367 584',
  'UpdatedDateUTC': datetime.datetime(2017, 2, 20, 18, 14, 30, 327000)}]
```

into this
```
Company Name      ,Address           ,Area     ,Postcode,State,Country  ,Phone     ,Email
Narromine Pharmacy,53 Dandaloo Street,Narromine,2830    ,NSW  ,Australia,0268891039,
```
"""
