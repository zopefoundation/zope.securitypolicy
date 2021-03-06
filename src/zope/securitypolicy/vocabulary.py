##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""Role Id Vocabulary.

This vocabulary provides role IDs.
"""
__docformat__ = 'restructuredtext'

import zope.component
from zope.interface import implementer, provider
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.interfaces import IGrantVocabulary


@provider(IVocabularyFactory)
class RoleIdsVocabulary(SimpleVocabulary):
    """A vocabular of role IDs.

    Term values are the role ID strings
    Term are stored by title

    To illustrate, we need to register the role IDs vocab:

    >>> from zope.schema import vocabulary
    >>> from zope.component.testing import setUp, tearDown
    >>> setUp()
    >>> vocabulary.setVocabularyRegistry(None)

    >>> registry = vocabulary.getVocabularyRegistry()
    >>> registry.register('Role Ids', RoleIdsVocabulary)

    Let's register some sample roles to test against them

    >>> from zope.securitypolicy.interfaces import IRole
    >>> from zope.securitypolicy.role import Role
    >>> from zope.component import provideUtility
    >>> provideUtility(Role('a_id','a_title'), IRole, 'a_id')
    >>> provideUtility(Role('b_id','b_title'), IRole, 'b_id')

    Let's lookup the roles using the vocabulary

    >>> vocab = registry.get(None, 'Role Ids')

    >>> vocab.getTermByToken('a_id').value
    u'a_id'
    >>> vocab.getTermByToken('b_id').value
    u'b_id'

    >>> tearDown()

    """

    def __init__(self, context):
        terms = []
        roles = zope.component.getUtilitiesFor(IRole, context)
        for name, role in roles:
            terms.append(SimpleTerm(name, name, name))
        super(RoleIdsVocabulary, self).__init__(terms)


@provider(IVocabularyFactory)
@implementer(IGrantVocabulary)
class GrantVocabulary(SimpleVocabulary):
    """A vocabular for getting the RadioWidget via the Choice field."""
