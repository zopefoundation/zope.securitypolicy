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
from zope.interface import implementer
from zope.authentication.interfaces import IAuthentication, PrincipalLookupError
from zope.security.interfaces import IPrincipal

@implementer(IAuthentication)
class DummyPrincipalRegistry(object):
    """Dummy principal registry that only implements getPrincipal
    and definePrincipal method that are needed for securitypolicy tests."""
    
    def __init__(self):
        self._principals = {}
        
    def getPrincipal(self, id):
        if id not in self._principals:
            raise PrincipalLookupError(id)
        return self._principals[id]

    def definePrincipal(self, id, title=u'', description=u''):
        p = DummyPrincipal(id, title, description)
        self._principals[id] = p
        return p

principalRegistry = DummyPrincipalRegistry()

@implementer(IPrincipal)
class DummyPrincipal(object):
    """Very simple principal implementation"""
    
    def __init__(self, id, title=u'', description=u''):
        self.id = id
        self.title = title
        self.description = description
