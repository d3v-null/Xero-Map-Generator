"""
Configuration.

Classes for parsing configuration files and command line arguments.
"""

import logging
import pprint
from argparse import SUPPRESS
from builtins import super
import os

from six import integer_types, string_types, text_type
from traitlets import Any, Bool, Float, Integer, Type, Unicode, Union, validate
from traitlets.config.configurable import Configurable
from traitlets.config.loader import (Config, ConfigFileNotFound,
                                     JSONFileConfigLoader,
                                     KVArgParseConfigLoader, LazyConfigValue,
                                     PyFileConfigLoader)

from . import DESCRIPTION, PKG_NAME
from .helper import TraitValidation
from .log import PKG_LOGGER, ROOT_LOGGER, log_level_quiet


class RichKVArgParseConfigLoader(KVArgParseConfigLoader):
    """ Extension of KVArgParseConfigLoader to handle complex argument parsing. """

    def __init__(self, aliases=None, flags=None, *super_args, **super_kwargs):
        """
        Create Rich KVArgParseConfigLoader object.

        Parameters
        ----------
        aliases : dict
            A dict of aliases for configurable traits.
            Keys are the short aliases, Values are a dict which contains the
            resolved trait and any extra arguments that should be passed to
            `argparse.add_argument`.
            Of the form:
            ```python
            {
                'alias' : {
                    'trait': 'Configurable.trait'
                    'add_args': ['extra_arguments'],
                    'add_kwargs': {
                        'keyword': 'extra_keyword_argument',
                    }
                }
            }`
            ```
        flags : dict
            A dict of flags, keyed by str name. Values are a dict which contains
            the flag value, and any extra arguments that should be passed to
            `argparse.add_argument`. The flag values can be Config objects,
            dicts, or "key=value" strings.  If Config or dict, when the flag
            is triggered, The flag is loaded as `self.config.update(m)`.
            Of the form:
            ```python
            {
                'flag' : {
                    'value': Config(trait='trait_value'),
                    'add_args': ['extra_arguments'],
                    'add_kwargs': {
                        'keyword': 'extra_keyword_argument',
                    }
                }
            }
            ```
        """
        self.alias_extensions = {}
        if aliases:
            super_aliases = {}
            for alias, values in aliases.items():
                assert 'trait' in values, "alias values must contain a trait"
                super_aliases[alias] = values.pop('trait')
                if values:
                    self.alias_extensions[alias] = values
            super_kwargs.update(aliases=super_aliases)

        self.flag_extensions = {}
        if flags:
            super_flags = {}
            for flag, values in flags.items():
                assert 'value' in values, "flag value dict must contain a value"
                super_flags[flag] = values.pop('value')
                if values:
                    self.flag_extensions[alias] = values
            super_kwargs.update(flags=super_flags)

        super().__init__(*super_args, **super_kwargs)

    def _add_arguments(self, aliases=None, flags=None):
        """ Override _add_arguments with alias and flag extensions. """
        self.alias_flags = {}
        # print aliases, flags
        if aliases is None:
            aliases = self.aliases
        if flags is None:
            flags = self.flags
        for key,value in aliases.items():
            add_args = self.alias_extensions.get(key, {}).get('add_args', [])
            if not add_args:
                add_args = ['-'+key] if len(key) is 1 else ['--'+key]
            add_kwargs = {
                'dest': value,
                'type': text_type
            }
            add_kwargs.update(
                self.alias_extensions.get(key, {}).get('add_kwargs', {})
            )
            if key in flags:
                # flags
                add_kwargs['nargs'] = '?'
            self.parser.add_argument(*add_args, **add_kwargs)
        for key, (value, help) in flags.items():
            if key in self.aliases:
                #
                self.alias_flags[self.aliases[key]] = value
                continue
            add_args = self.flag_extensions.get(key, {}).get('add_args', [])
            if not add_args:
                add_args = ['-'+key] if len(key) is 1 else ['--'+key]
            add_kwargs = {
                'dest': '_flags',
                'action': 'append_const',
                'const': value,
                'help': help
            }
            add_kwargs.update(
                self.flag_extensions.get(key, {}).get('add_kwargs', {})
            )
            self.parser.add_argument(*add_args, **add_kwargs)

class RichConfigurable(Configurable):
    # TODO: extra methods for auto generating add_args
    pass

class XeroApiConfig(RichConfigurable):
    rsa_key_path = Unicode(help='The path to the Xero API RSA key file')
    consumer_key = Unicode(help='The Xero API Consumer Key')

    @validate('rsa_key_path')
    def _valid_rsa_key_path(self, proposal):
        TraitValidation.path_exists(proposal['rsa_key_path'])
        return proposal['rsa_key_path']

    @validate('consumer_key')
    def _valid_consumer_key(self, proposal):
        TraitValidation.not_falsey(
            proposal['consumer_key'],
            "%s.%s" % (self.__class__, 'consumer_key')
        )

class LogConfig(RichConfigurable):
    stream_log_level = Unicode("WARNING", help="Set custom message output level")
    file_log_level = Unicode("DEBUG", help=SUPPRESS)
    log_file = Unicode('%s.log' % PKG_NAME, help=SUPPRESS)

class BaseConfig(RichConfigurable):
    contact_limit = Integer(
        default_value=0,
        help="Limit the number of contacts downloaded from the API"
    )

    config_file = Unicode(
        default_value="",
        help="Load extra config from file"
    )

    dump_file = Unicode(
        default_value="contacts.csv",
        help="Location where CSV data is dumped"
    )

class FilterConfig(RichConfigurable):
    contact_groups = Unicode(
        help="Filter by Xero contact group names separated by '|'"
    )

    @validate('contact_groups')
    def _valid_contact_groups(self, proposal):
        TraitValidation.not_falsey(
            proposal['contact_groups'],
            "%s.%s" % (self.__class__, 'contact_groups')
        )

    states = Unicode(
        "",
        help="Filter by main address state. Separate states with '|'"
    )

    @validate('states')
    def _valid_states(self, proposal):
        TraitValidation.not_falsey(
        proposal['states'],
        "%s.%s" % (self.__class__, 'states')
        )

    countries = Unicode(
        "",
        help="Filter by main address country. Separate countries with '|'"
    )

    @validate('countries')
    def _valid_countries(self, proposal):
        TraitValidation.not_falsey(
        proposal['countries'],
        "%s.%s" % (self.__class__, 'countries')
        )

def get_argparse_loader():
    # TODO: argparse loader args
    return RichKVArgParseConfigLoader(
        # TODO: generate alias argparse data from Configurable object directly
        aliases={
            'verbosity': {
                'trait': 'LogConfig.stream_log_level',
                'add_kwargs': {
                    'help': LogConfig.stream_log_level.help,
                    'default': text_type(LogConfig.stream_log_level.default_value),
                    'metavar': 'LEVEL'
                },
                'section': 'logging',
            },
            'log-level': {
                'trait': 'LogConfig.file_log_level',
                'add_kwargs': {
                    'help': LogConfig.file_log_level.help,
                    'default': text_type(LogConfig.file_log_level.default_value),
                    'metavar': 'LEVEL'
                },
                'section': 'logging',
            },
            'log-file': {
                'trait': 'LogConfig.log_file',
                'add_kwargs': {
                    'help': LogConfig.log_file.help,
                    'default': text_type(LogConfig.log_file.default_value),
                    'metavar': 'PATH'
                },
                'section': 'logging',
            },
            'xero-key-path': {
                'trait': 'XeroApiConfig.rsa_key_path',
                'add_kwargs': {
                    'help' : XeroApiConfig.rsa_key_path.help,
                    'metavar' : 'PATH'
                },
                'section': 'xero-api'
            },
            'xero-consumer-key': {
                'trait': 'XeroApiConfig.consumer_key',
                'add_kwargs': {
                    'help' : XeroApiConfig.consumer_key.help,
                    'metavar': 'KEY'
                },
                'section': 'xero-api'
            },
            'filter-contact-groups': {
                'trait': 'FilterConfig.contact_groups',
                'add_kwargs': {
                    'help' : FilterConfig.contact_groups.help,
                    'metavar': '"GROUP1|GROUP2"'
                },
                'section': 'filter'
            },
            'filter-states': {
                'trait': 'FilterConfig.states',
                'add_kwargs': {
                    'help' : FilterConfig.states.help,
                    'default': text_type(FilterConfig.states.default_value),
                    'metavar': '"STATE1|STATE2"'
                },
                'section': 'filter'
            },
            'filter-countries': {
                'trait': 'FilterConfig.countries',
                'add_kwargs': {
                    'help' : FilterConfig.countries.help,
                    'default': text_type(FilterConfig.countries.default_value),
                    'metavar': '"COUNTRY1|COUNTRY2"'
                },
                'section': 'filter'
            },
            'contact-limit': {
                'trait': 'BaseConfig.contact_limit',
                'add_kwargs': {
                    'help' : BaseConfig.contact_limit.help,
                    'default' : text_type(BaseConfig.contact_limit.default_value),
                    'metavar': 'LIMIT'
                },
            },
            'config-file': {
                'trait': 'BaseConfig.config_file',
                'add_kwargs': {
                    'help' : BaseConfig.config_file.help,
                    'default' : text_type(BaseConfig.config_file.default_value),
                    'metavar': 'FILE'
                },
            },
            'dump-file': {
                'trait': 'BaseConfig.dump_file',
                'add_kwargs': {
                    'help': BaseConfig.dump_file.help,
                    'default': text_type(BaseConfig.dump_file.default_value),
                    'metavar': 'FILE'
                }
            },
        },
        flags={
            'debug': {
                'value': ({'LogConfig': {'stream_log_level':'DEBUG'}}, 'display debug messages'),
                'add_args': ['-d', '--debug'],
                'section': 'logging',
            },
            'verbose': {
                'value': ({'LogConfig': {'stream_log_level':'INFO'}}, 'display extra information messages'),
                'add_args': ['-v', '--verbose'],
                'section': 'logging',
            },
            'quiet': {
                'value': ({'LogConfig': {'stream_log_level':'ERROR'}}, 'suppress warning messages'),
                'add_args': ['-q', '--quiet'],
                'section': 'logging',
            },
        },
        description=DESCRIPTION,
    )

def trait_defined_true(trait):
    """ Check if a trait is defined and not falsey. """
    if isinstance(trait, LazyConfigValue):
        return
    return trait

def load_cli_config(argv=None, has_extra_config=None):
    argparse_loader = get_argparse_loader()
    cli_config = argparse_loader.load_config(argv)
    if not any([
        has_extra_config,
        trait_defined_true(cli_config.BaseConfig.config_file),
        all([
            trait_defined_true(cli_config.XeroApiConfig.rsa_key_path),
            trait_defined_true(cli_config.XeroApiConfig.consumer_key)
        ])
    ]):
        ROOT_LOGGER.error("To connect to the Xero API, you must either specify a Xero API consumer key or a config file containing such a key")
        argparse_loader.parser.print_usage()
        exit()
    return cli_config

def load_file_config(extra_config_files=None, config_path=None):
    config = Config()
    extra_config_files = list(set([
        os.path.expanduser(conf) for conf in extra_config_files
    ]))
    for cf in extra_config_files:
        if cf[-3:] == ".py":
            loader = PyFileConfigLoader(cf, path=config_path)
        elif cf[-5:] == ".json":
            loader = JSONFileConfigLoader(cf, path=config_path)
        else:
            continue
        try:
            next_config = loader.load_config()
        except ConfigFileNotFound:
            pass
        except:
            raise
        else:
            config.merge(next_config)
    return config

def load_config(argv=None, extra_config_files=None, config_path=None):
    cli_config = load_cli_config(argv)
    if not log_level_quiet(cli_config.LogConfig.stream_log_level):
        ROOT_LOGGER.info("cli config is \n%s", pprint.pformat(cli_config))

    # TODO: generate config file list and config_path from cli_config
    extra_config_files = extra_config_files or []
    if cli_config.BaseConfig.config_file:
        extra_config_files.append(cli_config.BaseConfig.config_file)
    config = load_file_config(extra_config_files, config_path)

    if not log_level_quiet(cli_config.LogConfig.stream_log_level):
        ROOT_LOGGER.info("file config is \n%s", pprint.pformat(config))

    # merge cli_config
    config.merge(cli_config)
    if not log_level_quiet(cli_config.LogConfig.stream_log_level):
        ROOT_LOGGER.warning("config is \n%s", pprint.pformat(config))
    return config
