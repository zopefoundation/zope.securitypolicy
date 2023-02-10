##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""Grant info
"""
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer

from zope.securitypolicy.interfaces import IGrantInfo
from zope.securitypolicy.interfaces import Unset
from zope.securitypolicy.principalpermission import \
    AnnotationPrincipalPermissionManager
from zope.securitypolicy.principalrole import AnnotationPrincipalRoleManager
from zope.securitypolicy.rolepermission import AnnotationRolePermissionManager


prinperkey = AnnotationPrincipalPermissionManager.key
del AnnotationPrincipalPermissionManager

prinrolekey = AnnotationPrincipalRoleManager.key
del AnnotationPrincipalRoleManager

rolepermkey = AnnotationRolePermissionManager.key
del AnnotationRolePermissionManager


@implementer(IGrantInfo)
class AnnotationGrantInfo:

    def __init__(self, context):
        self._context = context
        annotations = IAnnotations(context, {})

        # by principals
        prinper = annotations.get(prinperkey)
        self.prinper = prinper._bycol if prinper is not None else {}

        # by principals
        prinrole = annotations.get(prinrolekey)
        self.prinrole = prinrole._bycol if prinrole is not None else {}

        # by permission
        roleper = annotations.get(rolepermkey)
        self.permrole = roleper._byrow if roleper is not None else {}

    def __bool__(self):
        return bool(self.prinper or self.prinrole or self.permrole)

    __nonzero__ = __bool__

    def principalPermissionGrant(self, principal, permission):
        prinper = self.prinper.get(principal, {})
        return prinper.get(permission, Unset)

    def getRolesForPermission(self, permission):
        permrole = self.permrole.get(permission, {})
        return list(permrole.items())

    def getRolesForPrincipal(self, principal):
        prinrole = self.prinrole.get(principal, {})
        return list(prinrole.items())
