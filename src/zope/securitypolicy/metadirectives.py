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
"""Grant Directive Schema
"""
from zope.configuration.fields import Tokens
from zope.interface import Interface
from zope.schema import Id
from zope.security.zcml import Permission, IPermissionDirective


class ISecurityObjectAssignmentDirective(Interface):
    """Abstract schema for security policy declarations."""

    principal = Id(
        title=u"Principal",
        description=u"Specifies the Principal to be mapped.",
        required=False)

    role = Id(
        title=u"Role",
        description=u"Specifies the Role to be mapped.",
        required=False)


class IGrantAllDirective(ISecurityObjectAssignmentDirective):
    """Grant Permissions to roles and principals and roles to principals."""


class ISpecificSecurityObjectAssignmentDirective(
        ISecurityObjectAssignmentDirective):
    """Abstract schema to set up one or more permissions"""

    permission = Permission(
        title=u"Permission",
        description=u"Specifies the Permission to be mapped.",
        required=False)

    permissions = Tokens(
        title=u"Permissions",
        description=(
            u"Specifies a whitespace-separated list of permissions to be "
            u"mapped."),
        value_type=Permission(),
        required=False)


class IGrantDirective(ISpecificSecurityObjectAssignmentDirective):
    """Grant Permissions to roles and principals and roles to principals."""


class IDenyDirective(ISpecificSecurityObjectAssignmentDirective):
    """Deny Permissions to roles and principals and roles to principals."""


class IDefineRoleDirective(IPermissionDirective):
    """Define a new role."""
