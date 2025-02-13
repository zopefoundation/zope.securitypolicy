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
"""Test handler for Annotation Role Permission Manager.
"""
import unittest

from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import provideAdapter
from zope.component import provideUtility
from zope.component.testing import PlacelessSetup
from zope.interface import implementer
from zope.security.interfaces import IPermission
from zope.security.permission import Permission

from zope.securitypolicy.interfaces import Allow
from zope.securitypolicy.interfaces import Deny
from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.interfaces import Unset
from zope.securitypolicy.role import Role
from zope.securitypolicy.rolepermission import AnnotationRolePermissionManager


@implementer(IAttributeAnnotatable)
class Manageable:
    pass


class Test(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        PlacelessSetup.setUp(self)
        provideAdapter(AttributeAnnotations)

        read = Permission('read', 'Read Something')
        provideUtility(read, IPermission, read.id)
        self.read = read.id

        write = Permission('write', 'Write Something')
        provideUtility(write, IPermission, write.id)
        self.write = write.id

        peon = Role('peon', 'Poor Slob')
        provideUtility(peon, IRole, peon.id)
        self.peon = peon.id

        manager = Role('manager', 'Supreme Being')
        provideUtility(manager, IRole, manager.id)
        self.manager = manager.id

    def testNormal(self):
        obj = Manageable()
        mgr = AnnotationRolePermissionManager(obj)
        mgr.grantPermissionToRole(self.read, self.manager)
        mgr.grantPermissionToRole(self.write, self.manager)
        mgr.grantPermissionToRole(self.write, self.manager)

        mgr.grantPermissionToRole(self.read, self.peon)

        l_ = list(mgr.getPermissionsForRole(self.manager))
        self.assertIn((self.read, Allow), l_)
        self.assertIn((self.write, Allow), l_)

        l_ = list(mgr.getPermissionsForRole(self.peon))
        self.assertEqual([(self.read, Allow)], l_)

        l_ = list(mgr.getRolesForPermission(self.read))
        self.assertIn((self.manager, Allow), l_)
        self.assertIn((self.peon, Allow), l_)

        l_ = list(mgr.getRolesForPermission(self.write))
        self.assertEqual(l_, [(self.manager, Allow)])

        mgr.denyPermissionToRole(self.read, self.peon)
        l_ = list(mgr.getPermissionsForRole(self.peon))
        self.assertEqual(l_, [(self.read, Deny)])

        mgr.unsetPermissionFromRole(self.read, self.peon)

        l_ = list(mgr.getRolesForPermission(self.read))
        self.assertEqual(l_, [(self.manager, Allow)])

        self.assertEqual(mgr.getSetting(self.read, self.peon), Unset)
        self.assertEqual(mgr.getSetting(self.read, self.peon, 1), 1)
