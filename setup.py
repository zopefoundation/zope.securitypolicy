##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# https://zopetoolkit.readthedocs.io/
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.securitypolicy package
"""
import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name='zope.securitypolicy',
    version='5.2.dev0',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    description='Default security policy for Zope3',
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('src', 'zope', 'securitypolicy', 'zopepolicy.txt')
        + '\n\n' +
        read('CHANGES.rst')),
    keywords="zope3 security policy",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    url='https://github.com/zopefoundation/zope.securitypolicy',
    license='ZPL-2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope'],
    python_requires='>=3.9',
    install_requires=[
        'persistent',
        'setuptools',
        'zope.annotation',
        'zope.authentication',
        'zope.component',
        'zope.configuration',
        'zope.i18nmessageid',
        'zope.interface >= 3.8',
        'zope.location',
        'zope.schema',
        'zope.security',
    ],
    extras_require=dict(
        test=[
            'zope.testing',
            'zope.testrunner',
        ],
        dublincore=[
            'zope.dublincore >= 3.7',
        ]),
    include_package_data=True,
    zip_safe=False,
)
