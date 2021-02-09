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

from setuptools import setup, find_packages, Extension


def run_setup(c_ext):
    if c_ext:
        kw = dict(
            ext_modules=[
                Extension(
                    'amazon.ion.ionc',
                    sources=['amazon/ion/ioncmodule.c'],
                    include_dirs=['amazon/ion', '/usr/local/include/ionc', '/usr/local/include/decNumber', '/usr/local/include'],
                    libraries=['ionc', 'decNumber'],
                    library_dirs=['/Users/cheqianh/Desktop/ion-c/ion-c/build/release/ionc',
                                  '/Users/cheqianh/Desktop/ion-c/ion-c/build/release/decNumber'],
                    extra_link_args=['-Wl,-rpath,/Users/cheqianh/Desktop/ion-c/ion-c/build/release/ionc/'],
                ),
            ],
        )
    else:
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
        **kw
    )


c_ext = True
run_setup(c_ext)