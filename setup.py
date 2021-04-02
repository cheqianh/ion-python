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
import shutil

from subprocess import check_call, call
import platform

from setuptools import setup, find_packages, Extension

from install import _install_ionc, _C_EXT_DEPENDENCY_INCLUDES_LOCATIONS, _C_EXT_DEPENDENCY_LIB_LOCATION
from setuptools.command.install import install
from distutils.sysconfig import get_python_lib
import setuptools.command.install_lib as ss

C_EXT = True
_OS = platform.system()
_WIN = _OS == 'Windows'
_MAC = _OS == 'Darwin'


class CustomInstall(install):
    def run(self):
        install.run(self)
        if _MAC:
            # Change C extension's dependency path to relative path of the loader (.so)
            file_path = ''
            lib_path = ''
            dir_path = 'build'
            for file in os.listdir(dir_path):
                if file[:5] == 'bdist':
                    file_path = os.path.join(dir_path, file)
            lib_dir = os.path.join(file_path, "wheel/amazon/ion/")
            for file in os.listdir(lib_dir):
                if file.endswith('.so'):
                    lib_path = os.path.join(lib_dir, file)
            call(['install_name_tool', '-change', '@rpath/libionc.1.0.3.dylib',
                  '@loader_path/ion-c-build/lib/libionc.dylib', lib_path])
            call(['install_name_tool', '-change', '@rpath/libdecNumber.dylib',
                  '@loader_path/ion-c-build/lib/libdecNumber.dylib', lib_path])


def run_setup(force_python_impl=False):
    if C_EXT:
        print('Ion-c build succeed. C extension is enabled!')
        kw = dict(
            ext_modules=[
                Extension(
                    'amazon.ion.ionc',
                    sources=['amazon/ion/ioncmodule.c'],
                    include_dirs=[
                                  # Mac
                                  'amazon/ion/ion-c-build/include',
                                  'amazon/ion/ion-c-build/include/ionc',
                                  'amazon/ion/ion-c-build/include/decNumber',
                                  # Windows
                                  # 'ion-c/ionc/include',
                                  # 'ion-c/decNumber/include'
                        ],
                    libraries=['ionc', 'decNumber'],
                    library_dirs=[
                                  # Mac
                                  'amazon/ion/ion-c-build/lib',
                                  # Windows
                                  # 'ion-c/ionc/Release', 'ion-c/decNumber/Release'
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
        version='0.7.89',
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
# try:
#     run_setup()
# except:
#     print('Build failed.')
#     print('Trying again with pure python implementation.')
#     run_setup(force_python_impl=True)


