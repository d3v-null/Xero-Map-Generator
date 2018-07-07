""" Main script for generating Map files. """
import os
import pprint
import sys

from xero_map_gen.config import load_config
from xero_map_gen.transport import XeroApiWrapper
from xero_map_gen.log import setup_logging, PKG_LOGGER

if __name__ == '__main__' and __package__ is None:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))



def main():
    """ main. """
    conf = load_config()
    setup_logging(**dict(conf.LogConfig))
    xero = XeroApiWrapper(**dict(conf.XeroApiConfig))
    map_contact_group_name = conf.BaseConfig.map_contact_group
    PKG_LOGGER.debug("map contact group name: %s", map_contact_group_name)
    map_contacts = xero.get_contacts_in_group(name=map_contact_group_name)
    PKG_LOGGER.debug("map contacts: %s", pprint.pformat(map_contacts))

    import pudb; pudb.set_trace()

if __name__ == '__main__':
    main()
