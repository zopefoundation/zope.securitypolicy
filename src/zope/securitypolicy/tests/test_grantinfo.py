##############################################################################
#
# Copyright (c) 2018 Zope Foundation and Contributors.
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

import unittest

from zope.annotation.interfaces import IAnnotations

from zope import interface
from zope.securitypolicy import grantinfo


# pylint:disable=protected-access

class Manager:

    def __init__(self):
        self._bycol = {}
        self._byrow = {}


@interface.implementer(IAnnotations)
class Annotated(dict):
    "Annotations"


class TestAnnotationGrantInfo(unittest.TestCase):

    def _makeContext(self):
        # Return a populated context with all three role managers
        prinper = Manager()
        prinrole = Manager()
        roleperm = Manager()

        context = Annotated()
        context[grantinfo.prinperkey] = prinper
        context[grantinfo.prinrolekey] = prinrole
        context[grantinfo.rolepermkey] = roleperm

        return context, prinper, prinrole, roleperm

    def _makeOne(self, context):
        return grantinfo.AnnotationGrantInfo(context)

    def test_no_annotations(self):
        # If we provide a context that has no IAnnotations,
        # we get defaults

        info = self._makeOne(None)

        self.assertFalse(info)
        self.assertEqual(grantinfo.Unset,
                         info.principalPermissionGrant(None, None))
        self.assertEqual([],
                         info.getRolesForPermission(None))
        self.assertEqual([],
                         info.getRolesForPrincipal(None))

    def test_manager_attributes(self):
        context, prinper, prinrole, roleperm = self._makeContext()
        info = self._makeOne(context)

        self.assertIs(info.prinper, prinper._bycol)
        self.assertIs(info.prinrole, prinrole._bycol)
        self.assertIs(info.permrole, roleperm._byrow)

    def test_principal_permission_grant(self):
        context, prinper, _, _ = self._makeContext()
        grants = prinper._bycol["principal"] = {}
        grant = grants["permission"] = object()

        info = self._makeOne(context)

        self.assertIs(grant,
                      info.principalPermissionGrant("principal", "permission"))

        self.assertIs(
            grantinfo.Unset,
            info.principalPermissionGrant(
                "principal",
                "other permission"))

        self.assertIs(
            grantinfo.Unset,
            info.principalPermissionGrant(
                "other principal",
                "other permission"))

    def test_roles_for_permission(self):
        context, _, _, roleperm = self._makeContext()
        grants = roleperm._byrow["permission"] = {}
        grants['key'] = 'value'

        info = self._makeOne(context)

        self.assertEqual([('key', 'value')],
                         info.getRolesForPermission('permission'))
        self.assertEqual([],
                         info.getRolesForPermission("other permission"))

    def test_roles_for_principal(self):
        context, _, prinper, _ = self._makeContext()
        grants = prinper._bycol["principal"] = {}
        grants['key'] = 'value'

        info = self._makeOne(context)

        self.assertEqual([('key', 'value')],
                         info.getRolesForPrincipal('principal'))
        self.assertEqual([],
                         info.getRolesForPrincipal("other principal"))
