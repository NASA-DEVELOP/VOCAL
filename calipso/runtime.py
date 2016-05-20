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
from constants import PATH
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
    # If the folder does exist, we must determine whether the VERSION.txt file is old or current
    try:
        with open(vocal_dir + r'\dat\VERSION.txt', 'r') as f:
            version = f.readline()  # read the version from the file within the appdata folder
    except:
        # if the program can't even open VERSION.txt, it must be a REALLY old version
        version = "NULL"
    if version != VERSION:
        # if the version does not match the program constants VERSION, we must ask the user whether
        # they wish to replace the old files with the new files found in the current versions runtime folder
        try:
            # check if the user has already made this decision within TRIGGERS.txt, if no decision has been made
            # e.g. the user opened it for the first time, the program will prompt him to make a decision. That
            # decision will be recorded within TRIGGERS.txt so the next time this program opens, it will read
            # the decision from TRIGGERS.txt
            with open(vocal_dir + r'\TRIGGERS.txt', 'r+') as g:
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
            # no decision was made, so set the mismatched version constant to true, now calipso will prompt the
            # user for a decision
            constants.MISMATCHED_VERSION = True # failing to open means TRIGGER.txt does not yet exist