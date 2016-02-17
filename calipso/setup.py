import os
import sys
from distutils.core import setup
import cx_Freeze
import matplotlib
import scipy
scipy_path = os.path.dirname(scipy.__file__)

base = "Console"

executable = [
    cx_Freeze.Executable("Calipso.py", base = base, icon="ico/broadcasting.ico")
]

build_exe_options = {"includes":["matplotlib.backends.backend_tkagg", "ccplot.algorithms",
                                 "ccplot.hdf"],
                     "packages":["Tkinter", "FileDialog"],
                     "include_files":[(matplotlib.get_data_path(), "mpl-data"),
                                      scipy_path],
                     "excludes": ["collections.abc"],
                     }

cx_Freeze.setup(
    name = "VOCAL",
    options = {"build_exe": build_exe_options},
    version = "0.0",
    description = "standalone",
    executables = executable
)
