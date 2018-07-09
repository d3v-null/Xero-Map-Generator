""" Communication with various APIs. """
import pprint
import time
from builtins import super

from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroRateLimitExceeded

from .contain import XeroContact
from .log import PKG_LOGGER
from .helper import dump_api_contacts, dump_contacts



class XeroApiWrapper(Xero):
    """ docstring for XeroApiWrapper. """
    sleep_time = 10
    max_attempts = 3

    def __init__(self, rsa_key_path, consumer_key):
        PKG_LOGGER.debug(
            "xero API args: rsa_key_path: %s; consumer_key: %s",
            rsa_key_path, consumer_key
        )

        with open(rsa_key_path) as key_file:
            rsa_key = key_file.read()

        credentials = PrivateCredentials(consumer_key, rsa_key)
        super().__init__(credentials)

    def rate_limit_retry_get(self, attribute, *args, **kwargs):
        attempts = 0
        sleep_time = self.sleep_time
        while attempts < self.max_attempts:
            try:
                return getattr(self, attribute).get(*args, **kwargs)
            except XeroRateLimitExceeded:
                PKG_LOGGER.info("API rate limit reached. Sleeping for %s seconds" % sleep_time)
                attempts += 1
                time.sleep(sleep_time)
                sleep_time += self.sleep_time
                continue
        raise UserWarning("Reached maximum number attempts (%s) for GET %s" % (self.max_attempts, attribute))

    def get_contacts_in_group(self, name=None, contact_group_id=None, limit=None):
        limit = limit or None
        assert any([name, contact_group_id]), "either name or contact_group_id must be specified"
        if contact_group_id is None:
            all_groups = self.contactgroups.all()
            PKG_LOGGER.debug("all xero contact groups: %s", pprint.pformat(all_groups))
            for contact_group in all_groups:
                if contact_group.get('Name', '') == name:
                    contact_group_id = contact_group.get('ContactGroupID')
        assert contact_group_id, "unable to find contact group ID for %s" % name
        group_data = self.contactgroups.get(contact_group_id)
        PKG_LOGGER.debug("group data: %s", pprint.pformat(group_data))
        # api_contacts = []
        contacts = []
        for contact_data in group_data[0]['Contacts']:
            if limit is not None and limit < 0:
                break

            contact_id = contact_data.get('ContactID', '')
            try:
                api_contact_data = self.rate_limit_retry_get('contacts', contact_id)
            except Exception:
                break
            assert len(api_contact_data) == 1
            api_contact_data = api_contact_data[0]
            # api_contacts.append(api_contact_data)
            assert api_contact_data, "empty api response for contact id %s" % contact_id
            PKG_LOGGER.debug("api contact: %s", pprint.pformat(contact_data))
            contact_obj = XeroContact(api_contact_data)
            PKG_LOGGER.debug("sanitized contact: %s", contact_obj)
            if not contact_obj.active:
                continue
            contacts.append(contact_obj)
            if limit is not None:
                limit -= 1
        # dump_api_contacts(api_contacts)
        dump_contacts(contacts)
        return contacts
