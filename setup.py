# -*- coding: utf-8 -*-
# -----------------------------------------------------------------
# Copyright 2013 - Kumina B.V./Pieter Lexis
# Copyright 2016 - Pieter Lexis
# Licensed under the terms of the GNU GPL version 3 or higher
# -----------------------------------------------------------------
"""
check_dnssec_validation

Check a zone to determine if the entire chain of trust down from the root is
secure.
"""

from setuptools import setup, find_packages

import check_dnssec_validation

setup(
    name="check-dnssec-validation",
    version=check_dnssec_validation.__version__,
    description=check_dnssec_validation.__doc__,
    long_description=__doc__,
    keywords="",

    author="Pieter Lexis",
    author_email="pieter@plexis.eu",
    license="GNU GPL 3",

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'check_dnssec_validation = check_dnssec_validation:main',
        ],
    },
)
