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
import sys
from subprocess import check_call, call

from setuptools import setup, find_packages, Extension

from amazon.ion.install import _install_ionc
from setuptools.command.install import install
from amazon.ion.simpleion import _FILE_PATH

C_EXT = True


class CustomInstall(install):
    def run(self):
        install.run(self)
        call(['pwd'])
        call(['ls'])
        if C_EXT:
            py_version = '%s.%s' % (sys.version_info[0], sys.version_info[1])
            paths = (s % (py_version) for s in (
                sys.prefix + '/lib/python%s/dist-packages/',
                sys.prefix + '/lib/python%s/site-packages/',
                sys.prefix + '/local/lib/python%s/dist-packages/',
                sys.prefix + '/local/lib/python%s/site-packages/',
                '/Library/Python/%s/site-packages/',
            ))

            for path in paths:
                if os.path.exists(path):
                    print('------- path: %s ---------' % path)
                    shutil.move('./ion-c', os.path.join(path, 'amazon', 'ion'))
                    break
        raise TypeError('----------------')


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
                    include_dirs=['amazon/ion', os.path.join(os.path.dirname(_FILE_PATH), 'ion-c/ionc/include/ionc'),
                                  os.path.join(os.path.dirname(_FILE_PATH), 'ion-c/ionc/include'),
                                  os.path.join(os.path.dirname(_FILE_PATH), 'ion-c/decNumber/include/decNumber'),
                                  os.path.join(os.path.dirname(_FILE_PATH), 'ion-c/decNumber/include')],
                    libraries=['ionc', 'decNumber'],
                    library_dirs=['ion-c/build/release/ionc', 'ion-c/build/release/decNumber',
                                  'ion-c/ionc/Release', 'ion-c/decNumber/Release'],
                    extra_link_args=['-Wl,-rpath,ion-c/build/release/ionc'],
                ),
            ],
        )
    else:
        print('Using pure python implementation.')
        kw = dict()


    setup(
        name='amazon.ion',
        version='0.7.37',
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


try:
    run_setup()
except:
    print('Build failed.')
    print('Trying again with pure python implementation.')
    run_setup(force_python_impl=True)


