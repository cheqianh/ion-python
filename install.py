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

_C_EXT_DEPENDENCY_DIR = abspath(join(dirname(os.path.abspath(__file__)), 'ion-c-build'))
_C_EXT_DEPENDENCY_LIB_LOCATION = abspath(join(_C_EXT_DEPENDENCY_DIR, 'lib'))
_C_EXT_DEPENDENCY_INCLUDES_LOCATIONS = abspath(join(_C_EXT_DEPENDENCY_DIR, 'include'))

_IONC_REPO_URL = "https://github.com/amzn/ion-c.git"
_IONC_DIR = abspath(join(dirname(os.path.abspath(__file__)), 'ion-c'))
_IONC_LOCATION = abspath(join(dirname(os.path.abspath(__file__)), 'ion-c', 'build', 'release'))
_IONC_INCLUDES_LOCATIONS = {
    'ionc': abspath(join(dirname(os.path.abspath(__file__)), 'ion-c', 'ionc', 'include', 'ionc')),
    'decNumber': abspath(
        join(dirname(os.path.abspath(__file__)), 'ion-c', 'decNumber', 'include', 'decNumber'))
}
_USERLIB_LOCATION = abspath(join(os.sep, 'usr', 'local', 'lib'))
_USERINCLUDE_LOCATION = abspath(join(os.sep, 'usr', 'local', 'include'))

_LIB_SUFFIX = '.dylib'
_LIB_PREFIX = 'lib'


def _get_lib_name(name):
    return '%s%s%s' % (_LIB_PREFIX, name, _LIB_SUFFIX)


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
    return os.path.exists(join(_C_EXT_DEPENDENCY_LIB_LOCATION, _get_lib_name(name)))


def _link_library(name):
    call(['ln', '-s', join(_C_EXT_DEPENDENCY_LIB_LOCATION, _get_lib_name(name)), join(_USERLIB_LOCATION, _get_lib_name(name))])

# TODO this method is prob not necessary
# def _link_includes(name):
#     includes_dir = join(_USERINCLUDE_LOCATION, name)
#     if not isdir(includes_dir):
#         call(['ln', '-s', join(_C_EXT_DEPENDENCY_INCLUDES_LOCATIONS, name), includes_dir])


def _download_ionc():
    try:
        # Create directory to store build output
        if not isdir(_C_EXT_DEPENDENCY_DIR):
            os.mkdir(_C_EXT_DEPENDENCY_DIR)
            os.mkdir(_C_EXT_DEPENDENCY_LIB_LOCATION)
            os.mkdir(_C_EXT_DEPENDENCY_INCLUDES_LOCATIONS)

        # Install ion-c
        if not isdir('./ion-c'):
            check_call(['git', 'clone', '--recurse-submodules', _IONC_REPO_URL, 'ion-c'])
        os.chdir('ion-c/')

        # Initialize submodule
        check_call(['git', 'submodule', 'update', '--init'])

        # Build ion-c
        if _WIN:
            _build_ionc_win()
        elif _MAC:
            _build_ionc_mac()
        os.chdir('../')
    except:
        if isdir(_C_EXT_DEPENDENCY_DIR):
            shutil.rmtree(_C_EXT_DEPENDENCY_DIR)
        if isdir(_IONC_DIR):
            shutil.rmtree(_IONC_DIR)
        print('ionc build error: Unable to build ion-c library.')
        return False


def _move_lib_mac(name):
    shutil.move(_IONC_INCLUDES_LOCATIONS[name], _C_EXT_DEPENDENCY_INCLUDES_LOCATIONS)

    dir_path = join(_IONC_LOCATION, name)
    for file in os.listdir(dir_path):
        file_path = join(dir_path, file)
        if file.endswith(_LIB_SUFFIX):
            shutil.move(file_path, _C_EXT_DEPENDENCY_LIB_LOCATION)


def _build_ionc_mac():
    # build ion-c
    check_call(['./build-release.sh'])

    # move ion-c to output dir
    _move_lib_mac('ionc')
    _move_lib_mac('decNumber')
    # link libraries to known place
    _link_library('ionc')
    # _link_includes('ionc')
    _link_library('decNumber')
    # _link_includes('decNumber')

    # move ion-c-build inside amazon/ion for distribution
    target_path = abspath(join(dirname(os.path.abspath(__file__)), '../amazon/ion/ion-c-build'))
    if os.path.isdir(target_path):
        shutil.rmtree(target_path)
    shutil.copytree(_C_EXT_DEPENDENCY_DIR, target_path)


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
