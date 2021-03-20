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

from setuptools import setup, find_packages, Extension

from amazon.ion.install import _install_ionc
from setuptools.command.install import install
from distutils.sysconfig import get_python_lib
import setuptools.command.install_lib as ss

C_EXT = True


class CustomInstall(install):
    def run(self):
        install.run(self)
        print(os.path.join(get_python_lib(), 'ion-c/ionc/include/ionc'))
        shutil.move('ion-c', os.path.join(get_python_lib(), 'amazon/ion'))
        raise TypeError('--------')


def run_setup(force_python_impl=False):
    # init and build ion-c module for C extension.
    C_EXT = _install_ionc() if not force_python_impl else False
    if C_EXT:
        print('Ion-c build succeed. C extension is enabled!')
        kw = dict(
            ext_modules=[
                Extension(
                    'amazon.ion.ionc',
                    sources=['amazon/ion/ioncmodule.c'],
                    include_dirs=['ion-c/ionc/include/ionc', 'ion-c/ionc/include',
                                  'ion-c/decNumber/include/decNumber', 'ion-c/decNumber/include',
                                  os.path.join(get_python_lib(), 'ion-c/ionc/include/ionc'),
                                  os.path.join(get_python_lib(), 'ion-c/ionc/include'),
                                  os.path.join(get_python_lib(), 'ion-c/decNumber/include/decNumber'),
                                  os.path.join(get_python_lib(), 'ion-c/decNumber/include')],
                    libraries=['ionc', 'decNumber'],
                    library_dirs=['ion-c/build/release/ionc', 'ion-c/build/release/decNumber',
                                  'ion-c/ionc/Release', 'ion-c/decNumber/Release',
                                  os.path.join(get_python_lib(), 'ion-c/build/release/ionc'),
                                  os.path.join(get_python_lib(), 'ion-c/build/release/decNumber'),
                                  os.path.join(get_python_lib(), 'ion-c/ionc/Release'),
                                  os.path.join(get_python_lib(), 'ion-c/decNumber/Release')],
                    extra_link_args=['-Wl,-rpath,ion-c/build/release/ionc',
                                     '-Wl,-rpath,%s' % os.path.join(get_python_lib(), 'ion-c/build/release/ionc')],
                ),
            ],
        )
    else:
        print('Using pure python implementation.')
        kw = dict()


    setup(
        name='amazon.ion',
        version='0.7.64',
        description='A Python implementation of Amazon Ion.',
        url='http://github.com/amzn/ion-python',
        author='Amazon Ion Team',
        author_email='ion-team@amazon.com',
        license='Apache License 2.0',

        packages=find_packages(exclude=['tests*']),
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


