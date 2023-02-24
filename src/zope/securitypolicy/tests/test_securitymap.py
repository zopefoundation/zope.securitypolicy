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
#############################################################################
"""Test SecurityMap implementations
"""
import unittest

from zope.security.management import endInteraction
from zope.security.management import getInteraction
from zope.security.management import newInteraction
from zope.security.management import setSecurityPolicy

from zope.securitypolicy.securitymap import PersistentSecurityMap
from zope.securitypolicy.securitymap import SecurityMap


class InteractionStub:
    invalidated = 0

    def invalidate_cache(self):
        self.invalidated += 1


class TestSecurityMap(unittest.TestCase):

    def setUp(self):
        self.oldpolicy = setSecurityPolicy(InteractionStub)
        newInteraction()

    def tearDown(self):
        endInteraction()
        setSecurityPolicy(self.oldpolicy)

    def _getSecurityMap(self):
        return SecurityMap()

    def test_addCell(self):
        map = self._getSecurityMap()
        self.assertEqual(getInteraction().invalidated, 0)
        map.addCell(0, 0, 'aa')
        self.assertEqual(getInteraction().invalidated, 1)
        self.assertEqual(map._byrow[0][0], 'aa')
        self.assertEqual(map._bycol[0][0], 'aa')

        map.addCell(1, 0, 'ba')
        self.assertEqual(getInteraction().invalidated, 2)
        self.assertEqual(map._byrow[1][0], 'ba')
        self.assertEqual(map._bycol[0][1], 'ba')

        map.addCell(5, 3, 'fd')
        self.assertEqual(getInteraction().invalidated, 3)
        self.assertEqual(map._byrow[5][3], 'fd')
        self.assertEqual(map._bycol[3][5], 'fd')

    def test_addCell_no_invalidation(self):

        class NoInvalidation:
            attrs = ()

            def __getattr__(self, name):
                self.attrs += (name,)
                return object.__getattr__(self, name)

        setSecurityPolicy(NoInvalidation)
        endInteraction()
        newInteraction()

        map = self._getSecurityMap()
        map.addCell(0, 0, 'aa')
        self.assertIn('invalidate_cache', getInteraction().attrs)

    def test_addCell_noninteger(self):
        map = self._getSecurityMap()
        map.addCell(0.3, 0.4, 'entry')
        self.assertEqual(map._byrow[0.3][0.4], 'entry')
        self.assertEqual(map._bycol[0.4][0.3], 'entry')

        marker = object()
        map.addCell('a', 'b', marker)
        self.assertEqual(map._byrow['a']['b'], marker)
        self.assertEqual(map._bycol['b']['a'], marker)

    def test_delCell(self):
        map = self._getSecurityMap()
        self.assertEqual(getInteraction().invalidated, 0)
        map._byrow[0] = {}
        map._bycol[1] = {}
        map._byrow[0][1] = 'aa'
        map._bycol[1][0] = 'aa'
        map.delCell(0, 1)
        self.assertEqual(getInteraction().invalidated, 1)
        self.assertEqual(map._byrow.get(0), None)
        self.assertEqual(map._bycol.get(1), None)

    def test_queryCell(self):
        map = self._getSecurityMap()
        map._byrow[0] = {}
        map._bycol[1] = {}
        map._byrow[0][1] = 'aa'
        map._bycol[1][0] = 'aa'

        marker = object()
        self.assertEqual(map.queryCell(0, 1), 'aa')
        self.assertEqual(map.queryCell(1, 0), None)
        self.assertEqual(map.queryCell(1, 0, marker), marker)

    def test_getCell(self):
        map = self._getSecurityMap()
        map._byrow[0] = {}
        map._bycol[1] = {}
        map._byrow[0][1] = 'aa'
        map._bycol[1][0] = 'aa'

        self.assertEqual(map.getCell(0, 1), 'aa')
        self.assertRaises(KeyError, map.getCell, 1, 0)

    def test_getRow(self):
        map = self._getSecurityMap()
        map._byrow[0] = {}
        map._byrow[0][1] = 'ab'
        map._byrow[0][2] = 'ac'
        map._byrow[1] = {}
        map._byrow[1][1] = 'bb'
        map._bycol[1] = {}
        map._bycol[1][0] = 'ab'
        map._bycol[1][1] = 'bb'
        map._bycol[2] = {}
        map._bycol[2][0] = 'ac'

        self.assertEqual(map.getRow(0), [(1, 'ab'), (2, 'ac')])
        self.assertEqual(map.getRow(1), [(1, 'bb')])
        self.assertEqual(map.getRow(2), [])

    def test_getCol(self):
        map = self._getSecurityMap()
        map._byrow[0] = {}
        map._byrow[0][1] = 'ab'
        map._byrow[0][2] = 'ac'
        map._byrow[1] = {}
        map._byrow[1][1] = 'bb'
        map._bycol[1] = {}
        map._bycol[1][0] = 'ab'
        map._bycol[1][1] = 'bb'
        map._bycol[2] = {}
        map._bycol[2][0] = 'ac'

        self.assertEqual(map.getCol(1), [(0, 'ab'), (1, 'bb')])
        self.assertEqual(map.getCol(2), [(0, 'ac')])
        self.assertEqual(map.getCol(0), [])

    def test_getAllCells(self):
        map = self._getSecurityMap()
        map._byrow[0] = {}
        map._byrow[0][1] = 'ab'
        map._byrow[0][2] = 'ac'
        map._byrow[1] = {}
        map._byrow[1][1] = 'bb'
        map._bycol[1] = {}
        map._bycol[1][0] = 'ab'
        map._bycol[1][1] = 'bb'
        map._bycol[2] = {}
        map._bycol[2][0] = 'ac'

        self.assertEqual(map.getCol(1), [(0, 'ab'), (1, 'bb')])
        self.assertEqual(map.getCol(2), [(0, 'ac')])
        self.assertEqual(map.getCol(0), [])


class TestPersistentSecurityMap(TestSecurityMap):

    def _getSecurityMap(self):
        return PersistentSecurityMap()


class TestAnnotationSecurityMap(unittest.TestCase):

    def test_changed_sets_map(self):
        from zope.annotation.interfaces import IAnnotations

        from zope.securitypolicy.securitymap import AnnotationSecurityMap

        class Context:
            def __init__(self):
                self.annotations = {}

            def __conform__(self, iface):
                if iface is IAnnotations:
                    return self.annotations

        class ASM(AnnotationSecurityMap):
            # 'key' is expected to be defined by subclasses
            key = 'key'

        context = Context()
        sec_map = ASM(context)
        # No key added yet.
        self.assertEqual(context.annotations, {})
        self.assertIsNone(sec_map.map)

        # Adding a cell sets the map
        sec_map.addCell('row', 'col', 'val')

        self.assertEqual(len(context.annotations), 1)
        self.assertIn(ASM.key, context.annotations)
        psm = context.annotations[ASM.key]
        self.assertIs(psm, sec_map.map)
