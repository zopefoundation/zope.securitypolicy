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

from doctest import DocFileSuite
import unittest
from zope.component import provideAdapter
from zope.component.testing import setUp as componentSetUp
from zope.component.testing import tearDown as componentTearDown
from zope.annotation.interfaces import IAnnotatable
from zope.annotation.attribute import AttributeAnnotations
from zope.security.management import endInteraction

from zope.securitypolicy.interfaces import IGrantInfo
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.interfaces import IPrincipalPermissionManager
from zope.securitypolicy.interfaces import IRolePermissionManager
from zope.securitypolicy.principalpermission import \
     AnnotationPrincipalPermissionManager
from zope.securitypolicy.principalrole import \
     AnnotationPrincipalRoleManager
from zope.securitypolicy.rolepermission import \
     AnnotationRolePermissionManager
from zope.securitypolicy.grantinfo import \
     AnnotationGrantInfo

class TestZCML(unittest.TestCase):

    def testMetaZCML(self):
        import zope.configuration
        import zope.securitypolicy
        zope.configuration.xmlconfig.file("meta.zcml", zope.securitypolicy)

    def testConfigureZCML(self):
        import zope.configuration
        import zope.securitypolicy
        zope.configuration.xmlconfig.file("configure.zcml", zope.securitypolicy)

    def testSecuritypolicyZCML(self):
        import zope.configuration
        import zope.securitypolicy
        zope.configuration.xmlconfig.file(
            "securitypolicy.zcml", zope.securitypolicy)


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
        unittest.makeSuite(TestZCML),
        ))
