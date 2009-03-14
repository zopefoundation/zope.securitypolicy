##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Role vocabluary doc tests.

$Id$
"""
import unittest
from zope.testing.doctest import DocTestSuite

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('zope.securitypolicy.vocabulary'),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
