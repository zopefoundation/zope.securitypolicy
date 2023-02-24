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
"""Tests the zope policy.
"""

import unittest
from doctest import DocFileSuite

from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAnnotatable
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import provideAdapter
from zope.component.testing import setUp as componentSetUp
from zope.component.testing import tearDown as componentTearDown
from zope.security.management import endInteraction
from zope.testing.cleanup import CleanUp

from zope import interface
from zope.securitypolicy import zopepolicy
from zope.securitypolicy.grantinfo import AnnotationGrantInfo
from zope.securitypolicy.interfaces import IGrantInfo
from zope.securitypolicy.interfaces import IPrincipalPermissionManager
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.interfaces import IRolePermissionManager
from zope.securitypolicy.principalpermission import \
    AnnotationPrincipalPermissionManager
from zope.securitypolicy.principalrole import AnnotationPrincipalRoleManager
from zope.securitypolicy.rolepermission import AnnotationRolePermissionManager


class TestZCML(CleanUp, unittest.TestCase):

    def testMetaZCML(self):
        import zope.configuration

        import zope.securitypolicy
        zope.configuration.xmlconfig.file("meta.zcml", zope.securitypolicy)

    def testConfigureZCML(self):
        import zope.configuration

        import zope.securitypolicy
        zope.configuration.xmlconfig.file(
            "configure.zcml", zope.securitypolicy)

    def testSecuritypolicyZCML(self):
        import zope.annotation
        import zope.configuration

        import zope.securitypolicy
        zope.configuration.xmlconfig.file(
            "configure.zcml", zope.annotation)

        zope.configuration.xmlconfig.file(
            "securitypolicy.zcml", zope.securitypolicy)

        settings = zopepolicy.settingsForObject(self)
        self.assertEqual(
            settings[0],
            ('(no name)', {})
        )
        self.assertEqual(
            settings[1][0],
            'global settings'
        )

        self.assertIn(
            'principalPermissions',
            settings[1][1]
        )
        self.assertIn(
            'rolePermissions',
            settings[1][1]
        )
        self.assertIn(
            'principalRoles',
            settings[1][1]
        )

        # Making us annotatable changes our data; we don't have anything
        # but we do have managers
        interface.alsoProvides(self, IAttributeAnnotatable)
        settings = zopepolicy.settingsForObject(self)
        self.assertEqual(
            settings[0], ('(no name)', {
                'principalPermissions': [],
                'principalRoles': [],
                'rolePermissions': []}))


class TestZopePolicy(CleanUp, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.policy = zopepolicy.ZopeSecurityPolicy()

    def test_checkPermission_system_user(self):
        from zope.security.management import system_user

        class Participation:
            principal = system_user
            interaction = None

        self.policy.add(Participation())

        self.assertTrue(self.policy.checkPermission('perm', self))

    def test_checkPermission_multiple_participations_for_same_id(self):

        class Principal:
            id = 'principal'

        class Participation:
            principal = Principal()
            interaction = None

        self.policy.add(Participation())
        self.policy.add(Participation())

        invoked_counter = []

        def cached_decision(self, *args):
            invoked_counter.append(args)
            return True

        self.policy.cached_decision = cached_decision
        self.assertTrue(self.policy.checkPermission('perm', self))
        self.assertEqual(1, len(invoked_counter))

    def test__findGroupsFor_seen(self):
        group_id = 'group'

        class Principal:
            groups = (group_id,)

        seen = {group_id}

        # Does nothing because we've already been seen
        self.assertEqual(
            self.policy._findGroupsFor(Principal(), None, seen),
            ()
        )

    def test__findGroupsFor_LookupError(self):
        # lookup errors are ignored
        from zope.authentication.interfaces import PrincipalLookupError

        class Principal:
            groups = ('group',)

        def getPrincipal(gid):
            raise PrincipalLookupError(gid)

        self.assertEqual(
            self.policy._findGroupsFor(Principal(), getPrincipal, []),
            ()
        )


def setUp(test):
    componentSetUp()
    endInteraction()
    provideAdapter(AttributeAnnotations)
    provideAdapter(AnnotationPrincipalPermissionManager, (IAnnotatable,),
                   IPrincipalPermissionManager)
    provideAdapter(AnnotationPrincipalRoleManager, (IAnnotatable,),
                   IPrincipalRoleManager)
    provideAdapter(AnnotationRolePermissionManager, (IAnnotatable,),
                   IRolePermissionManager)
    provideAdapter(AnnotationGrantInfo, (IAnnotatable,), IGrantInfo)


def test_suite():
    return unittest.TestSuite((
        DocFileSuite('zopepolicy.txt',
                     package='zope.securitypolicy',
                     setUp=setUp, tearDown=componentTearDown),
        unittest.defaultTestLoader.loadTestsFromName(__name__)
    ))
