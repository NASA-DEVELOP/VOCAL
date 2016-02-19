import os
import shutil

# Dump dependencies into appdata path if not already there
app_data_path = os.getenv('APPDATA')
vocal_dir = app_data_path + '\\vocal'    #AppData\Roaming
from os.path import expanduser
home = expanduser("~")
if not os.path.exists(vocal_dir):
    root_dir = '.'
    dat_dir = root_dir + '\..\dat'
    db_dir = root_dir + '\..\db'
    log_dir = root_dir + '\..\log'
    ico_dir = root_dir + '\..\ico'
    dat2_dir = root_dir + '\..\dat_'

    to_dat_dir = vocal_dir + '\dat'
    to_db_dir = vocal_dir + '\db'
    to_log_dir = vocal_dir + '\\fakedir\log'
    to_ico_dir = vocal_dir + '\\fakedir\ico'
    to_dat2_dir = vocal_dir + '\\fakedir\dat'

    shutil.copytree(dat_dir, to_dat_dir)
    shutil.copytree(db_dir, to_db_dir)
    shutil.copytree(log_dir, to_log_dir)
    shutil.copytree(ico_dir, to_ico_dir)
    shutil.copytree(dat2_dir, to_dat2_dir)
