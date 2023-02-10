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
""" Register security related configuration directives.
"""
from zope.component.zcml import utility
from zope.configuration.exceptions import ConfigurationError

from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.principalpermission import \
    principalPermissionManager as principal_perm_mgr
from zope.securitypolicy.principalrole import \
    principalRoleManager as principal_role_mgr
from zope.securitypolicy.role import Role
from zope.securitypolicy.rolepermission import \
    rolePermissionManager as role_perm_mgr


def grant(_context, principal=None, role=None, permission=None,
          permissions=None):
    nspecified = ((principal is not None)
                  + (role is not None)
                  + (permission is not None)
                  + (permissions is not None))
    permspecified = ((permission is not None)
                     + (permissions is not None))

    if nspecified != 2 or permspecified == 2:
        raise ConfigurationError(
            "Exactly two of the principal, role, and permission resp. "
            "permissions attributes must be specified")

    if permission:
        permissions = [permission]

    if principal and role:
        _context.action(
            discriminator=('grantRoleToPrincipal', role, principal),
            callable=principal_role_mgr.assignRoleToPrincipal,
            args=(role, principal),
        )
    elif principal and permissions:
        for permission in permissions:
            _context.action(
                discriminator=('grantPermissionToPrincipal',
                               permission,
                               principal),
                callable=principal_perm_mgr.grantPermissionToPrincipal,
                args=(permission, principal),
            )
    elif role and permissions:
        for permission in permissions:
            _context.action(
                discriminator=('grantPermissionToRole', permission, role),
                callable=role_perm_mgr.grantPermissionToRole,
                args=(permission, role),
            )


def deny(_context, principal=None, role=None, permission=None,
         permissions=None):
    nspecified = ((principal is not None)
                  + (role is not None)
                  + (permission is not None)
                  + (permissions is not None))
    permspecified = ((permission is not None)
                     + (permissions is not None))

    if nspecified != 2 or permspecified == 2:
        raise ConfigurationError(
            "Exactly two of the principal, role, and permission resp. "
            "permissions attributes must be specified")

    if permission:
        permissions = [permission]

    if principal and role:
        _context.action(
            discriminator=('denyRoleFromPrincipal', role, principal),
            callable=principal_role_mgr.removeRoleFromPrincipal,
            args=(role, principal),
        )
    elif principal and permissions:
        for permission in permissions:
            _context.action(
                discriminator=('denyPermissionToPrincipal',
                               permission,
                               principal),
                callable=principal_perm_mgr.denyPermissionToPrincipal,
                args=(permission, principal),
            )
    elif role and permissions:
        for permission in permissions:
            _context.action(
                discriminator=('denyPermissionToRole', permission, role),
                callable=role_perm_mgr.denyPermissionToRole,
                args=(permission, role),
            )


def grantAll(_context, principal=None, role=None):
    """Grant all permissions to a role or principal
    """
    nspecified = ((principal is not None)
                  + (role is not None))

    if nspecified != 1:
        raise ConfigurationError(
            "Exactly one of the principal and role attributes "
            "must be specified")

    if principal:
        _context.action(
            discriminator=('grantAllPermissionsToPrincipal',
                           principal),
            callable=principal_perm_mgr.grantAllPermissionsToPrincipal,
            args=(principal, ),
        )
    else:
        _context.action(
            discriminator=('grantAllPermissionsToRole', role),
            callable=role_perm_mgr.grantAllPermissionsToRole,
            args=(role, ),
        )


def defineRole(_context, id, title, description=''):
    role = Role(id, title, description)
    utility(_context, IRole, role, name=id)
