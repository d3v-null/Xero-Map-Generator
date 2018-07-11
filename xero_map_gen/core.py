import os
import pprint
import sys

from xero_map_gen.config import load_config
from xero_map_gen.transport import XeroApiWrapper
from xero_map_gen.log import setup_logging, PKG_LOGGER
from xero_map_gen.contain import XeroContact

def main():
    """ main. """
    conf = load_config()
    setup_logging(**dict(conf.LogConfig))
    xero = XeroApiWrapper(**dict(conf.XeroApiConfig))
    map_contact_groups = conf.FilterConfig.contact_groups.split('|')
    PKG_LOGGER.debug("map contact groups: %s", map_contact_groups)
    contact_limit = conf.BaseConfig.contact_limit or None
    PKG_LOGGER.debug("contact limit: %s", contact_limit)
    map_contacts = xero.get_contacts_in_groups(names=map_contact_groups, limit=contact_limit)
    for filter_attr, contact_attr in [
        ('states', 'main_address_state'),
        ('countries', 'main_address_country'),
    ]:
        if filter_attr not in conf.FilterConfig:
            continue
        filter_values = [value.upper() for value in getattr(conf.FilterConfig, filter_attr).split('|')]
        filtered_contacts = []
        for contact in map_contacts:
            contact_value = getattr(contact,contact_attr)
            if not contact_value:
                PKG_LOGGER.warn("Contact has no value for %s filter: %s" % (
                    filter_attr,
                    pprint.pformat(contact.flatten_verbose())
                ))
            if contact_value.upper() in filter_values:
                filtered_contacts.append(contact)
        if not filtered_contacts:
            PKG_LOGGER.error("No contacts matching %s filter" % filter_attr)
        map_contacts = filtered_contacts

    # TODO: validate addresses
    PKG_LOGGER.info("map contacts: \n%s", XeroContact.dump_contacts_sanitized_table(map_contacts))

    # XeroContact.dump_contacts_raw_csv(map_contacts)
    # XeroContact.dump_contacts_verbose_csv(map_contacts)
    XeroContact.dump_contacts_sanitized_csv(map_contacts, dump_path=conf.BaseConfig.dump_file)

    PKG_LOGGER.warning("saved %d contacts to %s" % (len(map_contacts), conf.BaseConfig.dump_file))