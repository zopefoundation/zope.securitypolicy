=========
 Changes
=========

6.0 (2025-09-12)
================

- Replace ``pkg_resources`` namespace with PEP 420 native namespace.


5.1 (2025-02-14)
================

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7, 3.8.


5.0 (2023-02-24)
================

- Add support for Python 3.9, 3.10, 3.11.

- Drop support for Python 2.7, 3.5, 3.6.


4.3.2 (2021-03-19)
==================

- Add support for Python 3.8.

- Drop support for Python 3.4.

- Fix some test imports to use the proper imports from
  ``zope.interface`` instead of ``zope.component``.

4.3.1 (2018-10-11)
==================

- Use current location for `IRegistered` and `IUnregistered` interface.


4.3.0 (2018-08-27)
==================

- Add support for Python 3.7.

- Drop support for Python 3.3.

- Drop support for ``python setup.py test``.

- Make ``SecurityMap`` and ``AnnotationGrantInfo`` have proper truth
  behaviour on Python 3; previously they were always true.

- Make ``AnnotationGrantInfo`` consistently return lists instead of
  dict views on Python 3.

- Make ``AnnotationSecurityMap`` (and objects derived from it, such as
  ``AnnotationPrincipalPermissionManager`` and the role managers) more
  efficient when adding or removing cells before they have been
  persisted. They now avoid some unnecessary object copying.

4.2.0 (2017-08-24)
==================

- Add ``<zope:deny>`` directive, which is a mirror of the ``<zope:grant>``
  directive.

- Add support for Python 3.6.


4.1.0 (2016-11-05)
==================

- Add support for Python 3.5.

- Drop support for Python 2.6.

- Add support to grant multiple permissions with one ZCML statement. Example::

    <grant
      role="my-role"
      permissions="zope.foo
                   zope.bar" />


4.0.0 (2014-12-24)
==================

- Add support for PyPy.  (PyPy3 is pending release of a fix for:
  https://bitbucket.org/pypy/pypy/issue/1946)

- Add support for Python 3.4.

- Add support for testing on Travis.


4.0.0a1 (2013-02-22)
====================

- Add support for Python 3.3.

- Replace deprecated ``zope.interface.classProvides`` usage with equivalent
  ``zope.interface.provider`` decorator.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.


3.7.0 (2010-09-25)
==================

- LP #131115: Clean up inconsistency in ``getSetting`` interface definitions
  and actual usage for the various security maps.

- LP #564525:  fix permission moved from ``zope.app.dublincore`` namespace
  to ``zope.dublincore``.

- Remove unused imports and pep8 cleanup.

- Use doctest module instead of the deprecated zope.testing.doctest.

- AnnotationGrantInfo implements IGrantInfo.

- Add test extra to declare test dependency on ``zope.component [test]``.

- Add an extra named ``dublincore`` to express optional dependency on
  ``zope.dublincore >= 3.7``.

- Add tests for ZCML files making sure they include everything they need.


3.6.1 (2009-07-24)
==================

- Make tests work when the default and Zope vocabulary registry compete in the
  cleanup.

3.6.0 (2009-03-14)
==================

- Change ``zope.app.security`` dependency to the new ``zope.authentication``
  package, dropping a big number of unused dependencies.

- Get rid of ``zope.app.testing`` and other testing dependencices.

- Add ``ZODB3`` to install dependencies, because we use ``Persistent``
  class. We didn't fail before, because it was installed implicitly.

3.5.1 (2009-03-10)
==================

- Don't depend on the ``hook`` extra of zope.component, as we don't need
  it explicitly.

- Import security settings (Allow, Deny, Unset) in the ``interfaces``
  module from the ``zope.securitypolicy.settings``, added in previous
  release instead of old ``zope.app.security.settings``.
  The ``zope.app.security`` will be adapted to import them from
  ``zope.securitypolicy.interfaces``.

- Use ``_z_instances`` instead of ``__instances__`` for storing instances
  for ``zope.securitypolicy.settings.PermissionSetting`` singleton
  implementation, because __*__ name pattern is reserved for special
  names in python.

- Add security protections for the ``PermissionSetting``.

- Improve documentation formatting, add it to the package's long
  description.

- Remove unneeded dependencies.

- Remove old zpkg-related files and zcml slugs.

3.5.0 (2009-01-31)
==================

- Include settings that were previously imported from zope.app.security.

3.4.2 (2009-01-28)
==================

- Change mailing list address to zope-dev at zope.org. Fix package
  homepage to the pypi page.

- Fix test in buildout which still depended on zope.app.securitypolicy
  by mistake.

- Remove explicit dependency on zope.app.form from ``setup.py``; nothing
  in the code directly depends on this.

3.4.1 (2008-06-02)
==================

- Fix reference to deprecated security policy from ZCML.

3.4.0 (2007-09-25)
==================

- Initial documented release
