#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import subprocess
from pathlib import Path

from . import util
from .util import plog


def cs_verify(dir_path):
    command = "codesign --verify --verbose '{}'".format(dir_path)
    is_success = True
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        is_success = False

    return is_success


def cs_info(dir_path):
    # codesign --display --verbose --verify
    command = "codesign -d -vv '{}'".format(dir_path)
    is_success = True
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        is_success = False
        output = str(e)

    return is_success, output


def run_codesign(dir_path, entitlements_path=None):
    p12_id = "B975F4F03263A3A29F0BC84910303364EB9B25E0"
    # codesign --force --sign <keychain_SHA1> --entitlements <app_path> <entitlements_path>
    command = "codesign -fs '{}' '{}'".format(p12_id, dir_path)
    if entitlements_path:
        command += " --entitlements '{}'".format(entitlements_path)
    plog(command)
    if util.IS_QUIET:
        subprocess.check_output(command, shell=True)
    else:
        subprocess.check_call(command, shell=True)


def cs_app(app_path, entitlements_path=None):
    app_path = Path(app_path)
    for tmp_file_path in app_path.iterdir():
        if tmp_file_path.name == 'Frameworks':
            for sub_fw_path in tmp_file_path.iterdir():
                if sub_fw_path.suffix == ".framework":
                    run_codesign(sub_fw_path)

    run_codesign(app_path, entitlements_path)
