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
import unittest
from pickle import Pickler, Unpickler

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    # Py3: New location.
    from io import BytesIO

from zope.securitypolicy.interfaces import Allow


class Test(unittest.TestCase):

    def testPickleUnpickle(self):
        s = BytesIO()
        p = Pickler(s)
        p.dump(Allow)
        s.seek(0)
        u = Unpickler(s)
        newAllow = u.load()

        self.assertTrue(newAllow is Allow)


def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(Test)

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
