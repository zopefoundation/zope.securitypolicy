##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Security setting constants.

The `Allow`, `Deny`, and `Unset` constants are exposed by the
`zope.securitypolicy.interfaces` module, and should be imported
from there.
"""


class PermissionSetting(object):
    """PermissionSettings should be considered as immutable.
    They can be compared by identity. They are identified by
    their name.
    """

    def __new__(cls, name, description=None):
        """Keep a dict of PermissionSetting instances, indexed by
        name. If the name already exists in the dict, return that
        instance rather than creating a new one.
        """
        instances = cls.__dict__.get('_z_instances')
        if instances is None:
            cls._z_instances = instances = {}
        it = instances.get(name)
        if it is None:
            instances[name] = it = object.__new__(cls)
            it._init(name, description)
        return it

    def _init(self, name, description):
        self.__name = name
        self.__description = description

    def getDescription(self):
        return self.__description

    def getName(self):
        return self.__name

    def __str__(self):
        return "PermissionSetting: %s" % self.__name

    __repr__ = __str__

# register PermissionSettings to be symbolic constants by identity,
# even when pickled and unpickled.
import copy_reg
copy_reg.constructor(PermissionSetting)
copy_reg.pickle(PermissionSetting,
                PermissionSetting.getName,
                PermissionSetting)


Allow = PermissionSetting('Allow',
    'Explicit allow setting for permissions')

Deny = PermissionSetting('Deny',
    'Explicit deny setting for permissions')

Unset = PermissionSetting('Unset',
    'Unset constant that denotes no setting for permission')
