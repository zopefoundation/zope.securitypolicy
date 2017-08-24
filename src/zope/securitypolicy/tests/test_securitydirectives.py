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
"""Security Directives Tests
"""
import unittest

import zope.component
from zope.configuration import xmlconfig
from zope.configuration.config import ConfigurationConflictError
from zope.configuration.exceptions import ConfigurationError
from zope.security.interfaces import IPermission
from zope.security.permission import Permission

from zope.component.testing import PlacelessSetup
from zope.authentication.interfaces import IAuthentication

from zope.securitypolicy.role import Role
from zope.securitypolicy.interfaces import Allow, Deny
from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.rolepermission import \
    rolePermissionManager as role_perm_mgr
from zope.securitypolicy.principalpermission import \
    principalPermissionManager as principal_perm_mgr
from zope.securitypolicy.principalrole import \
    principalRoleManager as principal_role_mgr
import zope.securitypolicy.tests
from zope.securitypolicy.tests import principalRegistry


def defineRole(id, title=None, description=None):
    role = Role(id, title, description)
    zope.component.provideUtility(role, IRole, role.id)
    return role


class TestBase(PlacelessSetup):

    def setUp(self):
        super(TestBase, self).setUp()
        zope.component.provideUtility(principalRegistry, IAuthentication)


class TestRoleDirective(TestBase, unittest.TestCase):

    def testRegister(self):
        xmlconfig.file("role.zcml", zope.securitypolicy.tests)

        role = zope.component.getUtility(IRole, "zope.Everyperson")
        self.assertTrue(role.id.endswith('Everyperson'))
        self.assertEqual(role.title, 'Tout le monde')
        self.assertEqual(role.description,
                         'The common man, woman, person, or thing')

    def testDuplicationRegistration(self):
        self.assertRaises(ConfigurationConflictError, xmlconfig.file,
                          "role_duplicate.zcml", zope.securitypolicy.tests)


class TestSecurityGrantMapping(TestBase, unittest.TestCase):

    def setUp(self):
        super(TestSecurityGrantMapping, self).setUp()
        zope.component.provideUtility(Permission('zope.Foo', ''),
                                      IPermission, 'zope.Foo')
        zope.component.provideUtility(Permission('zope.Qwer', ''),
                                      IPermission, 'zope.Qwer')
        zope.component.provideUtility(Permission('zope.Qux', ''),
                                      IPermission, 'zope.Qux')
        defineRole("zope.Bar", '', '')
        defineRole("zope.Fox", '', '')
        principalRegistry.definePrincipal("zope.Blah", '', '')
        principalRegistry.definePrincipal("zope.One", '', '')
        self.context = xmlconfig.file(
            "mapping.zcml", zope.securitypolicy.tests)

    def test_PermRoleMap(self):
        roles = role_perm_mgr.getRolesForPermission("zope.Foo")
        perms = role_perm_mgr.getPermissionsForRole("zope.Bar")

        self.assertEqual(len(roles), 1)
        self.assertTrue(("zope.Bar", Allow) in roles)

        self.assertEqual(len(perms), 1)
        self.assertTrue(("zope.Foo", Allow) in perms)

    def test_PermRoleMap_multiple(self):
        quer_roles = role_perm_mgr.getRolesForPermission("zope.Qwer")
        qux_roles = role_perm_mgr.getRolesForPermission("zope.Qux")
        perms = role_perm_mgr.getPermissionsForRole("zope.Fox")

        self.assertEqual(len(quer_roles), 1)
        self.assertTrue(("zope.Fox", Allow) in quer_roles)

        self.assertEqual(len(qux_roles), 1)
        self.assertTrue(("zope.Fox", Allow) in qux_roles)

        self.assertEqual(len(perms), 2)
        self.assertTrue(("zope.Qwer", Allow) in perms)
        self.assertTrue(("zope.Qux", Allow) in perms)

    def test_PermRoleMap_does_not_allow_permission_and_permissions(self):
        with self.assertRaises(ConfigurationError):
            xmlconfig.file(
                "permission_and_permissions.zcml", zope.securitypolicy.tests)

    def test_PermPrincipalMap(self):
        principals = principal_perm_mgr.getPrincipalsForPermission("zope.Foo")
        perms = principal_perm_mgr.getPermissionsForPrincipal("zope.Blah")

        self.assertEqual(len(principals), 1)
        self.assertTrue(("zope.Blah", Allow) in principals)

        self.assertEqual(len(perms), 1)
        self.assertTrue(("zope.Foo", Allow) in perms)

    def test_PermPrincipalMap_multiple(self):
        quer_principals = principal_perm_mgr.getPrincipalsForPermission(
            "zope.Qwer")
        qux_principals = principal_perm_mgr.getPrincipalsForPermission(
            "zope.Qux")
        perms = principal_perm_mgr.getPermissionsForPrincipal("zope.One")

        self.assertEqual(len(quer_principals), 1)
        self.assertTrue(("zope.One", Allow) in quer_principals)

        self.assertEqual(len(qux_principals), 1)
        self.assertTrue(("zope.One", Allow) in qux_principals)

        self.assertEqual(len(perms), 2)
        self.assertTrue(("zope.Qwer", Allow) in perms)
        self.assertTrue(("zope.Qux", Allow) in perms)

    def test_RolePrincipalMap(self):
        principals = principal_role_mgr.getPrincipalsForRole("zope.Bar")
        roles = principal_role_mgr.getRolesForPrincipal("zope.Blah")

        self.assertEqual(len(principals), 1)
        self.assertTrue(("zope.Blah", Allow) in principals)

        self.assertEqual(len(roles), 1)
        self.assertTrue(("zope.Bar", Allow) in roles)


class TestSecurityGrantAllMapping(TestBase, unittest.TestCase):

    def setUp(self):
        super(TestSecurityGrantAllMapping, self).setUp()
        zope.component.provideUtility(Permission('zope.Qwer', ''),
                                      IPermission, 'zope.Qwer')
        zope.component.provideUtility(Permission('zope.Qux', ''),
                                      IPermission, 'zope.Qux')
        defineRole("zope.Bar", '', '')
        principalRegistry.definePrincipal("zope.Blah", '', '')
        self.context = xmlconfig.file(
            "grantall_mapping.zcml", zope.securitypolicy.tests)

    def test_PermRoleMap(self):
        perms = role_perm_mgr.getPermissionsForRole("zope.Bar")

        self.assertEqual(len(perms), 2)
        self.assertTrue(("zope.Qwer", Allow) in perms)
        self.assertTrue(("zope.Qux", Allow) in perms)

    def test_PermPrincipalMap(self):
        perms = principal_perm_mgr.getPermissionsForPrincipal("zope.Blah")

        self.assertEqual(len(perms), 2)
        self.assertTrue(("zope.Qwer", Allow) in perms)
        self.assertTrue(("zope.Qux", Allow) in perms)

    def test_principal_and_role_not_allowed(self):
        with self.assertRaises(ConfigurationError):
            xmlconfig.string('''
                 <configure xmlns="http://namespaces.zope.org/zope">
                   <grantAll
                       role="zope.Bar"
                       principal="zope.Blah"
                       />
                 </configure>
            ''', context=self.context)


class TestSecurityDenyMapping(TestBase, unittest.TestCase):

    def setUp(self):
        super(TestSecurityDenyMapping, self).setUp()
        zope.component.provideUtility(Permission('zope.Foo', ''),
                                      IPermission, 'zope.Foo')
        zope.component.provideUtility(Permission('zope.Qwer', ''),
                                      IPermission, 'zope.Qwer')
        zope.component.provideUtility(Permission('zope.Qux', ''),
                                      IPermission, 'zope.Qux')
        defineRole("zope.Bar", '', '')
        defineRole("zope.Fox", '', '')
        principalRegistry.definePrincipal("zope.Blah", '', '')
        principalRegistry.definePrincipal("zope.One", '', '')
        self.context = xmlconfig.file(
            "deny_mapping.zcml", zope.securitypolicy.tests)

    def test_PermRoleMap(self):
        roles = role_perm_mgr.getRolesForPermission("zope.Foo")
        perms = role_perm_mgr.getPermissionsForRole("zope.Bar")

        self.assertEqual(len(roles), 1)
        self.assertTrue(("zope.Bar", Deny) in roles)

        self.assertEqual(len(perms), 1)
        self.assertTrue(("zope.Foo", Deny) in perms)

    def test_PermRoleMap_multiple(self):
        quer_roles = role_perm_mgr.getRolesForPermission("zope.Qwer")
        qux_roles = role_perm_mgr.getRolesForPermission("zope.Qux")
        perms = role_perm_mgr.getPermissionsForRole("zope.Fox")

        self.assertEqual(len(quer_roles), 1)
        self.assertTrue(("zope.Fox", Deny) in quer_roles)

        self.assertEqual(len(qux_roles), 1)
        self.assertTrue(("zope.Fox", Deny) in qux_roles)

        self.assertEqual(len(perms), 2)
        self.assertTrue(("zope.Qwer", Deny) in perms)
        self.assertTrue(("zope.Qux", Deny) in perms)

    def test_PermRoleMap_does_not_allow_permission_and_permissions(self):
        with self.assertRaises(ConfigurationError):
            xmlconfig.string('''
                 <configure xmlns="http://namespaces.zope.org/zope">
                   <deny
                       permission="zope.Foo"
                       permissions="zope.Qwer zope.Qux"
                       />
                 </configure>
            ''', context=self.context)

    def test_cannot_specify_all_three_object_types(self):
        with self.assertRaises(ConfigurationError):
            xmlconfig.string('''
                 <configure xmlns="http://namespaces.zope.org/zope">
                   <deny
                       role="zope.Bar"
                       principal="zope.Blah"
                       permission="zope.Foo"
                       />
                 </configure>
            ''', context=self.context)
    def test_PermPrincipalMap(self):
        principals = principal_perm_mgr.getPrincipalsForPermission("zope.Foo")
        perms = principal_perm_mgr.getPermissionsForPrincipal("zope.Blah")

        self.assertEqual(len(principals), 1)
        self.assertTrue(("zope.Blah", Deny) in principals)

        self.assertEqual(len(perms), 1)
        self.assertTrue(("zope.Foo", Deny) in perms)

    def test_PermPrincipalMap_multiple(self):
        quer_principals = principal_perm_mgr.getPrincipalsForPermission(
            "zope.Qwer")
        qux_principals = principal_perm_mgr.getPrincipalsForPermission(
            "zope.Qux")
        perms = principal_perm_mgr.getPermissionsForPrincipal("zope.One")

        self.assertEqual(len(quer_principals), 1)
        self.assertTrue(("zope.One", Deny) in quer_principals)

        self.assertEqual(len(qux_principals), 1)
        self.assertTrue(("zope.One", Deny) in qux_principals)

        self.assertEqual(len(perms), 2)
        self.assertTrue(("zope.Qwer", Deny) in perms)
        self.assertTrue(("zope.Qux", Deny) in perms)

    def test_RolePrincipalMap(self):
        principals = principal_role_mgr.getPrincipalsForRole("zope.Bar")
        roles = principal_role_mgr.getRolesForPrincipal("zope.Blah")

        self.assertEqual(len(principals), 1)
        self.assertTrue(("zope.Blah", Deny) in principals)

        self.assertEqual(len(roles), 1)
        self.assertTrue(("zope.Bar", Deny) in roles)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestRoleDirective),
        unittest.makeSuite(TestSecurityGrantMapping),
        unittest.makeSuite(TestSecurityGrantAllMapping),
        unittest.makeSuite(TestSecurityDenyMapping),
    ))

if __name__ == '__main__':
    unittest.main()
