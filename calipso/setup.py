from distutils.core import setup
import numpy
import py2exe
import matplotlib
import zmq.libzmq
import FileDialog

datafiles = [('lib', (zmq.libzmq.__file__,))]
datafiles.extend(matplotlib.get_py2exe_datafiles())

setup(
    console=["Calipso.py"],
    options={
      'py2exe': {
          'packages': ['FileDialog', 'sqlalchemy', 'scipy.linalg',
                       'scipy.special._ufuncs_cxx'],
          'includes': ['zmq.backend.cython'],
          'excludes': ['zmq.libzmq'],
          'dll_excludes': ['libzmq.pyd'],
      },
    },
    data_files=datafiles)

