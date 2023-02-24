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
"""Security Settings Tests
"""
import pickle
import unittest

from zope.securitypolicy.interfaces import Allow


class Test(unittest.TestCase):

    def testPickleUnpickle(self):
        for prot in range(0, pickle.HIGHEST_PROTOCOL):
            s = pickle.dumps(Allow, prot)
            newAllow = pickle.loads(s)

            self.assertIs(newAllow, Allow)

    def testDescription(self):
        self.assertEqual("Explicit allow setting for permissions",
                         Allow.getDescription())

    def testName(self):
        self.assertEqual("Allow",
                         Allow.getName())

    def testStr(self):
        self.assertEqual("PermissionSetting: Allow",
                         str(Allow))
