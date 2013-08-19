#!/usr/bin/env python
#
#   Copyright (c) 2013 In-Q-Tel, Inc/Lab41, All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from setuptools import setup

setup(
    name='hemlock',
    version='0.1.0',
    author=u'Charlie Lewis',
    author_email='charliel@lab41.org',
    description='Hemlock is a way of providing a common data access layer.',
    url='http://lab41.github.io/Hemlock',
    packages=['hemlock', 'hemlock.clients', 'hemlock.load_scripts'],
    scripts=['bin/hemlock', 'scripts/ci/setup_env.sh'],
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    keywords='hemlock metadata cache heterogeneous'.split(),
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Environment :: Other Environment'
    ],
    data_files=[
        ('', ['LICENSE.txt'])
    ],
    install_requires=[
        'MySQL-python',
        'couchbase',
        'texttable'
    ]
)