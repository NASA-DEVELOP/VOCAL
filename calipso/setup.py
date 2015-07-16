#===============================================================================
# 
# Created on Jul 16, 2015
# 
# @author: nqian
# 
#===============================================================================

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    
options = {
           'build_exe':{
                        'packages': ['tkinter',
                                     'matplotlib',
                                     'webbrowser',
                                     
                                     ]
                        }
           }
    
executables = [Executable('Calipso.py', base=base)]

setup(name='test',
      version='0.1',
      description='a test',
      executables=executables
    )