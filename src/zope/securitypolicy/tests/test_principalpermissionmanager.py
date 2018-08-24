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
"""Test handler for PrincipalPermissionManager module.
"""
import unittest

from zope.component import provideUtility
from zope.component.testing import PlacelessSetup
from zope.security.interfaces import IPermission
from zope.security.permission import Permission

from zope.authentication.interfaces import IAuthentication

from zope.securitypolicy.interfaces import Allow, Deny, Unset
from zope.securitypolicy.principalpermission import \
    principalPermissionManager as manager
from zope.securitypolicy.tests import principalRegistry


def definePermission(id, title=None, description=None):
    perm = Permission(id, title, description)
    provideUtility(perm, IPermission, perm.id)
    return perm


class Test(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(Test, self).setUp()
        provideUtility(principalRegistry, IAuthentication)

    def _make_principal(self, id=None, title=None):
        p = principalRegistry.definePrincipal(
            id or 'APrincipal',
            title or 'A Principal')
        return p.id

    def testUnboundPrincipalPermission(self):
        permission = definePermission('APerm', 'title').id
        principal = self._make_principal()
        self.assertEqual(manager.getPrincipalsForPermission(permission), [])
        self.assertEqual(manager.getPermissionsForPrincipal(principal), [])

    def test_invalidPrincipal(self):
        permission = definePermission('APerm', 'title').id
        self.assertRaises(ValueError,
                          manager.grantPermissionToPrincipal,
                          permission, 'principal')

    def testPrincipalPermission(self):
        permission = definePermission('APerm', 'title').id
        principal = self._make_principal()
        # check that an allow permission is saved correctly
        manager.grantPermissionToPrincipal(permission, principal)
        self.assertEqual(manager.getPrincipalsForPermission(permission),
                         [(principal, Allow)])
        self.assertEqual(manager.getPermissionsForPrincipal(principal),
                         [(permission, Allow)])
        # check that the allow permission is removed.
        manager.unsetPermissionForPrincipal(permission, principal)
        self.assertEqual(manager.getPrincipalsForPermission(permission), [])
        self.assertEqual(manager.getPermissionsForPrincipal(principal), [])
        # now put a deny in there, check it's set.
        manager.denyPermissionToPrincipal(permission, principal)
        self.assertEqual(manager.getPrincipalsForPermission(permission),
                         [(principal, Deny)])
        self.assertEqual(manager.getPermissionsForPrincipal(principal),
                         [(permission, Deny)])
        # test for deny followed by allow . The latter should override.
        manager.grantPermissionToPrincipal(permission, principal)
        self.assertEqual(manager.getPrincipalsForPermission(permission),
                         [(principal, Allow)])
        self.assertEqual(manager.getPermissionsForPrincipal(principal),
                         [(permission, Allow)])
        # check that allow followed by allow is just a single allow.
        manager.grantPermissionToPrincipal(permission, principal)
        self.assertEqual(manager.getPrincipalsForPermission(permission),
                         [(principal, Allow)])
        self.assertEqual(manager.getPermissionsForPrincipal(principal),
                         [(permission, Allow)])
        # check that two unsets in a row quietly ignores the second one.
        manager.unsetPermissionForPrincipal(permission, principal)
        manager.unsetPermissionForPrincipal(permission, principal)
        self.assertEqual(manager.getPrincipalsForPermission(permission), [])
        self.assertEqual(manager.getPermissionsForPrincipal(principal), [])
        # check the result of getSetting() when it's empty.
        self.assertEqual(manager.getSetting(permission, principal), Unset)
        # check the result of getSetting() when it's empty and a default
        # passed in
        self.assertEqual(manager.getSetting(permission, principal, 1), 1)
        # check the result of getSetting() when it's allowed.
        manager.grantPermissionToPrincipal(permission, principal)
        self.assertEqual(manager.getSetting(permission, principal), Allow)
        # check the result of getSetting() when it's denied.
        manager.denyPermissionToPrincipal(permission, principal)
        self.assertEqual(manager.getSetting(permission, principal), Deny)

    def testManyPermissionsOnePrincipal(self):
        perm1 = definePermission('Perm One', 'title').id
        perm2 = definePermission('Perm Two', 'title').id
        prin1 = self._make_principal()
        manager.grantPermissionToPrincipal(perm1, prin1)
        manager.grantPermissionToPrincipal(perm2, prin1)
        perms = manager.getPermissionsForPrincipal(prin1)
        self.assertEqual(len(perms), 2)
        self.assertTrue((perm1, Allow) in perms)
        self.assertTrue((perm2, Allow) in perms)
        manager.denyPermissionToPrincipal(perm2, prin1)
        perms = manager.getPermissionsForPrincipal(prin1)
        self.assertEqual(len(perms), 2)
        self.assertTrue((perm1, Allow) in perms)
        self.assertTrue((perm2, Deny) in perms)
        perms = manager.getPrincipalsAndPermissions()
        self.assertTrue((perm1, prin1, Allow) in perms)
        self.assertTrue((perm2, prin1, Deny) in perms)

    def testAllPermissions(self):
        perm1 = definePermission('Perm One', 'title').id
        perm2 = definePermission('Perm Two', 'title').id
        prin1 = self._make_principal()
        manager.grantAllPermissionsToPrincipal(prin1)
        perms = manager.getPermissionsForPrincipal(prin1)
        self.assertEqual(len(perms), 2)
        self.assertTrue((perm1, Allow) in perms)
        self.assertTrue((perm2, Allow) in perms)

    def testManyPrincipalsOnePermission(self):
        perm1 = definePermission('Perm One', 'title').id
        prin1 = self._make_principal()
        prin2 = self._make_principal('Principal 2', 'Principal Two')
        manager.grantPermissionToPrincipal(perm1, prin1)
        manager.denyPermissionToPrincipal(perm1, prin2)
        principals = manager.getPrincipalsForPermission(perm1)
        self.assertEqual(len(principals), 2)
        self.assertTrue((prin1, Allow) in principals)
        self.assertTrue((prin2, Deny) in principals)
