# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at:
#
#    http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the
# License.

# Python 2/3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from os.path import dirname, join
from subprocess import call
import platform
from setuptools import setup, find_packages, Extension
from setuptools.command.install import install

C_EXT = True
_OS = platform.system()
_WIN = _OS == 'Windows'
_MAC = _OS == 'Darwin'
_BDIST = 'bdist'
_SHARED_OBJECT_SUFFIX = '.so'
_IONC_LIB_LOCATION = join(dirname(os.path.abspath(__file__)), 'amazon/ion/ion-c-build/lib')


def change_c_extension_lib_path():
    """
    Change C extension (.so)'s dependency search path to relative path (@loader_path)
    """
    if not _MAC:
        return
    dir_path = join(dirname(os.path.abspath(__file__)), 'build')
    for folder in os.listdir(dir_path):
        if folder[:5] == 'bdist':
            lib_dir = os.path.join(dir_path, folder, "wheel/amazon/ion/")
            for file in os.listdir(lib_dir):
                if file.endswith(_SHARED_OBJECT_SUFFIX):
                    for lib in os.listdir(_IONC_LIB_LOCATION):
                        call(['install_name_tool', '-change', '@rpath/%s' % lib,
                              '@loader_path/ion-c-build/lib/%s' % lib, os.path.join(lib_dir, file)])


class CustomInstall(install):
    def run(self):
        install.run(self)
        change_c_extension_lib_path()


def run_setup():
    if C_EXT:
        print('C extension is enabled!')
        kw = dict(
            ext_modules=[
                Extension(
                    'amazon.ion.ionc',
                    sources=['amazon/ion/ioncmodule.c'],
                    include_dirs=['amazon/ion/ion-c-build/include',
                                  'amazon/ion/ion-c-build/include/ionc',
                                  'amazon/ion/ion-c-build/include/decNumber',
                    ],
                    libraries=['ionc', 'decNumber'],
                    library_dirs=['amazon/ion/ion-c-build/lib',
                    ],
                    extra_link_args=['-Wl,-rpath,%s' % 'amazon/ion/ion-c-build/lib'],   # Used for Dev
                ),
            ],
        )
    else:
        print('Using pure python implementation.')
        kw = dict()


    setup(
        name='amazon.ion',
        version='0.7.0',
        description='A Python implementation of Amazon Ion.',
        url='http://github.com/amzn/ion-python',
        author='Amazon Ion Team',
        author_email='ion-team@amazon.com',
        license='Apache License 2.0',

        packages=find_packages(exclude=['tests*']),
        include_package_data=True,
        namespace_packages=['amazon'],

        install_requires=[
            'six',
        ],

        setup_requires=[
            'pytest-runner',
        ],

        tests_require=[
            'pytest',
        ],
        cmdclass={'install': CustomInstall},
        **kw
    )


run_setup()
