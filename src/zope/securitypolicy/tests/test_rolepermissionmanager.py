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
"""Test handler for RolePermissionManager module.
"""
import unittest

from zope.component import provideUtility
from zope.component.testing import PlacelessSetup
from zope.security.interfaces import IPermission
from zope.security.permission import Permission

from zope.securitypolicy.role import Role
from zope.securitypolicy.interfaces import Allow, Deny, Unset
from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.rolepermission import \
    rolePermissionManager as manager


def defineRole(id, title=None, description=None):
    role = Role(id, title, description)
    provideUtility(role, IRole, role.id)
    return role


def definePermission(id, title=None, description=None):
    perm = Permission(id, title, description)
    provideUtility(perm, IPermission, perm.id)
    return perm


class Test(PlacelessSetup, unittest.TestCase):

    def testUnboundRolePermission(self):
        permission = definePermission('APerm', 'aPerm title').id
        role = defineRole('ARole', 'A Role').id
        self.assertEqual(manager.getRolesForPermission(permission), [])
        self.assertEqual(manager.getPermissionsForRole(role), [])
        self.assertEqual(manager.getSetting(permission, role), Unset)
        self.assertEqual(manager.getSetting(permission, role, 1), 1)

    def testRolePermission(self):
        permission = definePermission('APerm', 'aPerm title').id
        role = defineRole('ARole', 'A Role').id
        manager.grantPermissionToRole(permission, role)
        self.assertEqual(manager.getRolesForPermission(permission),
                         [(role, Allow)])
        self.assertEqual(manager.getPermissionsForRole(role),
                         [(permission, Allow)])

    def testManyPermissionsOneRole(self):
        perm1 = definePermission('Perm One', 'P1').id
        perm2 = definePermission('Perm Two', 'P2').id
        perm3 = definePermission('Perm Three', 'P3').id
        role1 = defineRole('Role One', 'Role #1').id
        perms = manager.getPermissionsForRole(role1)
        self.assertEqual(len(perms), 0)
        manager.grantPermissionToRole(perm1, role1)
        manager.grantPermissionToRole(perm2, role1)
        manager.grantPermissionToRole(perm2, role1)
        manager.denyPermissionToRole(perm3, role1)
        perms = manager.getPermissionsForRole(role1)
        self.assertEqual(len(perms), 3)
        self.assertTrue((perm1, Allow) in perms)
        self.assertTrue((perm2, Allow) in perms)
        self.assertTrue((perm3, Deny) in perms)
        manager.unsetPermissionFromRole(perm1, role1)
        perms = manager.getPermissionsForRole(role1)
        self.assertEqual(len(perms), 2)
        self.assertTrue((perm2, Allow) in perms)

    def testAllPermissions(self):
        perm1 = definePermission('Perm One', 'P1').id
        perm2 = definePermission('Perm Two', 'P2').id
        perm3 = definePermission('Perm Three', 'P3').id
        role1 = defineRole('Role One', 'Role #1').id
        perms = manager.getPermissionsForRole(role1)
        self.assertEqual(len(perms), 0)
        manager.grantAllPermissionsToRole(role1)
        perms = manager.getPermissionsForRole(role1)
        self.assertEqual(len(perms), 3)
        self.assertTrue((perm1, Allow) in perms)
        self.assertTrue((perm2, Allow) in perms)
        self.assertTrue((perm3, Allow) in perms)

    def testManyRolesOnePermission(self):
        perm1 = definePermission('Perm One', 'title').id
        role1 = defineRole('Role One', 'Role #1').id
        role2 = defineRole('Role Two', 'Role #2').id
        roles = manager.getRolesForPermission(perm1)
        self.assertEqual(len(roles), 0)
        manager.grantPermissionToRole(perm1, role1)
        manager.grantPermissionToRole(perm1, role2)
        manager.grantPermissionToRole(perm1, role2)
        manager.denyPermissionToRole(perm1, role1)
        roles = manager.getRolesForPermission(perm1)
        self.assertEqual(len(roles), 2)
        self.assertFalse((role1, Allow) in roles)
        self.assertTrue((role1, Deny) in roles)
        self.assertTrue((role2, Allow) in roles)
        manager.unsetPermissionFromRole(perm1, role1)
        roles = manager.getRolesForPermission(perm1)
        self.assertEqual(len(roles), 1)
        self.assertTrue((role2, Allow) in roles)

    def test_invalidRole(self):
        self.assertRaises(ValueError,
                          manager.grantPermissionToRole, 'perm1', 'role1'
                          )
        perm1 = definePermission('Perm One', 'title').id
        self.assertRaises(ValueError,
                          manager.grantPermissionToRole, perm1, 'role1'
                          )


def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(Test)

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
