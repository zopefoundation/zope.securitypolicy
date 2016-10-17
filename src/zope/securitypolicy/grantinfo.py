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
from zope.securitypolicy.interfaces import Unset
from zope.securitypolicy.interfaces import IGrantInfo

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
class AnnotationGrantInfo(object):

    prinper = prinrole = permrole = {}

    def __init__(self, context):
        self._context = context
        annotations = IAnnotations(context, None)
        if annotations is not None:

            prinper = annotations.get(prinperkey)
            if prinper is not None:
                self.prinper = prinper._bycol  # by principals

            prinrole = annotations.get(prinrolekey)
            if prinrole is not None:
                self.prinrole = prinrole._bycol  # by principals

            roleper = annotations.get(rolepermkey)
            if roleper is not None:
                self.permrole = roleper._byrow  # by permission

    def __nonzero__(self):
        return bool(self.prinper or self.prinrole or self.permrole)

    def principalPermissionGrant(self, principal, permission):
        prinper = self.prinper.get(principal)
        if prinper:
            return prinper.get(permission, Unset)
        return Unset

    def getRolesForPermission(self, permission):
        permrole = self.permrole.get(permission)
        if permrole:
            return permrole.items()
        return ()

    def getRolesForPrincipal(self, principal):
        prinrole = self.prinrole.get(principal)
        if prinrole:
            return prinrole.items()
        return ()
