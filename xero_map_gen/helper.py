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

def expand_relative_path(path, dir):
    path = os.path.expandvars(path)
    path = os.path.normpath(path)
    path = os.path.expanduser(path)
    if not path.startswith('/') and dir:
        dir = os.path.expandvars(dir)
        dir = os.path.normpath(dir)
        dir = os.path.expanduser(dir)
        path = os.path.join(dir, path)
    return os.path.abspath(path)
