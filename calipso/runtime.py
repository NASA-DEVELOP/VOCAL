##########################
#
#
#   @Author: Katie Moore
##########################

import os
import shutil
from os.path import expanduser
import constants
from constants import VERSION
import tkMessageBox

def copy_runtime(vocal_dir, copy_db, delete_existing):
    root_dir = '.'
    dat_dir = root_dir + r'\..\dat'
    db_dir = root_dir + r'\..\db'
    log_dir = root_dir + r'\..\log'
    ico_dir = root_dir + r'\..\ico'
    dat2_dir = root_dir + r'\..\dat_'

    to_dat_dir = vocal_dir + r'\dat'
    to_db_dir = vocal_dir + r'\db'
    to_log_dir = vocal_dir + r'\fakedir\log'
    to_ico_dir = vocal_dir + r'\fakedir\ico'
    to_dat2_dir = vocal_dir + r'\fakedir\dat'

    if delete_existing:
        shutil.rmtree(to_dat_dir)
        if copy_db:
            shutil.rmtree(to_db_dir)
        shutil.rmtree(to_log_dir)
        shutil.rmtree(to_ico_dir)
        shutil.rmtree(to_dat2_dir)

    shutil.copytree(dat_dir, to_dat_dir)
    if copy_db:
        shutil.copytree(db_dir, to_db_dir)
    shutil.copytree(log_dir, to_log_dir)
    shutil.copytree(ico_dir, to_ico_dir)
    shutil.copytree(dat2_dir, to_dat2_dir)

def get_appdata_vocal_dir():
    app_data_path = os.getenv('APPDATA')
    dir = app_data_path + r'\vocal'
    return dir

# Dump dependencies into appdata path if not already there
vocal_dir = get_appdata_vocal_dir()
if not os.path.exists(vocal_dir):
    copy_runtime(vocal_dir, True, False)
else:
    # the folder may already exist, but may be an older version
    with open(vocal_dir + r'\db\VERSION.txt', 'r') as f:
        version = f.readline()
    if version != VERSION:
        try:
            with open(PATH + r'\TRIGGERS.txt', 'r+') as g:
                flag = g.readline()
            if flag == constants.COPY_ALL:
                copy_runtime(vocal_dir, True, True)
            elif flag == constants.COPY_NO_DB:
                copy_runtime(vocal_dir, False, True)
            elif flag == constants.COPY_PASS:
                constants.MISMATCHED_VERSION = True
                g.seek(0)
                g.write(constants.COPY_PASS)
            except:
                constants.MISMATCHED_VERSION = True # if no file exists , we assume version is bad