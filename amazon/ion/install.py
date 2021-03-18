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
import platform
import shutil
import sys
from subprocess import call, Popen, PIPE, check_call
from os.path import join, abspath, isdir, dirname

_PYPY = hasattr(sys, 'pypy_translation_info')
_OS = platform.system()
_WIN = _OS == 'Windows'
_MAC = _OS == 'Darwin'

_IONC_REPO_URL = "https://github.com/amzn/ion-c.git"
_IONC_LOCATION = abspath(join(dirname(os.path.abspath(__file__)), '..', '..', 'ion-c', 'build', 'release'))
_IONC_INCLUDES_LOCATIONS = {
    'ionc': abspath(join(dirname(os.path.abspath(__file__)), '..', '..', 'ion-c', 'ionc', 'include', 'ionc')),
    'decNumber': abspath(
        join(dirname(os.path.abspath(__file__)), '..', '..', 'ion-c', 'decNumber', 'include', 'decNumber'))
}
_USERLIB_LOCATION = abspath(join(os.sep, 'usr', 'local', 'lib'))
_USERINCLUDE_LOCATION = abspath(join(os.sep, 'usr', 'local', 'include'))

_LIB_SUFFIX = '.dylib'
_LIB_PREFIX = 'lib'


def _library_exists():
    if _MAC:
        return _library_exists_mac('ionc') and _library_exists_mac('decNumber')
    elif _WIN:
        return _library_exists_win()


def _library_exists_win():
    if not os.path.exists('ion-c/ionc/Release/ionc.lib') \
            or not os.path.exists('ion-c/decNumber/Release/decNumber.lib'):
        return False
    return True


def _library_exists_mac(name):
    proc = Popen(['ld', '-l%s' % name], stderr=PIPE, stdout=PIPE)
    stdout, stderr = proc.communicate()
    return (b'library not found' not in stdout and
            b'library not found' not in stderr and
            os.path.exists('ion-c/build/release/ionc') and
            os.path.exists('ion-c/build/release/decNumber'))


def _link_library(name):
    lib_name = '%s%s%s' % (_LIB_PREFIX, name, _LIB_SUFFIX)
    call(['ln', '-s', join(_IONC_LOCATION, name, lib_name), join(_USERLIB_LOCATION, lib_name)])


def _link_includes(name):
    includes_dir = join(_USERINCLUDE_LOCATION, name)
    if not isdir(includes_dir):
        call(['ln', '-s', _IONC_INCLUDES_LOCATIONS[name], includes_dir])


def _download_ionc():
    try:
        print('000000')
        # Install ion-c
        if not isdir('./ion-c'):
            check_call(['git', 'clone', '--recurse-submodules', _IONC_REPO_URL, 'ion-c'])
            print('1111111')
        os.chdir('ion-c/')
        # Initialize submodule
        check_call(['git', 'submodule', 'update', '--init'])
        print('222222222')
        # Builds ion-c
        if _WIN:
            _build_ionc_win()
        elif _MAC:
            _build_ionc_mac()
            print('33333333')
        os.chdir('../')
        shutil.move('./ion-c', './amazon/ion/')
    except:
        print('ionc build error: Unable to build ion-c library.')


def _build_ionc_mac():
    # build ion-c
    check_call(['./build-release.sh'])
    # link libraries to known place
    _link_library('ionc')
    _link_includes('ionc')
    _link_library('decNumber')
    _link_includes('decNumber')


def _build_ionc_win():
    # check_call('cmake -G \"Visual Studio 15 2017 Win64\"')
    check_call('cmake -G \"Visual Studio 16 2019\"')
    check_call('cmake --build . --config Release')


def _check_dependencies():
    try:
        check_call(['git', '--version'])
        check_call(['cmake', '--version'])
        # TODO add more dependency check here
    except:
        print('ion-c build error: Missing dependencies.')
        return False
    return True


def _install_ionc():
    if _PYPY:  # This is pointless if running with PyPy, which doesn't support CPython extensions anyway.
        return False

    if not _check_dependencies():
        return False

    if not _library_exists():
        if not _download_ionc():
            return False

    return True


if __name__ == "__main__":
    res = _install_ionc()
