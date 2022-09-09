from distutils.core import setup
import py2exe
import matplotlib
import sys
sys.setrecursionlimit(5000)
DATA = [
    ('dat',
     ['C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/CALIPSO.jpg',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/calipso-aerosol_subtype.cmap',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/calipso-backscatter.cmap',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/calipso-depolar.cmap',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/calipso-horizontalaveraging.cmap',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/calipso-icewaterphase.cmap',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/calipso-vfm.cmap',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/CALIPSO_A_Train.jpg',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/config.json',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/depolarization_ratio.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/grey.jpg',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/dat/lidar_backscatter.png']),
    ('log',
     ['C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/log/trace.log']),
    ('ico',
     ['C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/back.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/broadcasting.gif',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/broadcasting.ico',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/broadcasting.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/broadcasting.xbm',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/cog.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/cursorhand.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/cursorhighlight.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/edit.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/eraser.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/extract.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/focus.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/forward.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/freedraw.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/hide.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/home.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/load.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/magnify.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/paint.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/plotcursor.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/polygon.png',
      'C:/Users/cpampalo/PycharmProjects/VOCAL/calipso/ico/save.png'])
]

DATA.extend(matplotlib.get_py2exe_datafiles())

setup(
    windows=[{'script': 'Calipso.py'}],
    options={
        "py2exe":{
            "dist_dir": "C:/Users/cpampalo/Desktop/build",
            'excludes': [
                'jinja2.asyncsupport',
                '_gtkagg',
                '_qt4agg',
                '_agg2',
                '_cairo',
                '_cocoaagg',
                '_fltkagg',
                '_gtk',
                '_gtkcairo',
                '_wx'
            ],
            'packages': [
                'FileDialog',
                'scipy',
                'sqlalchemy',
                'matplotlib'
            ],
            'includes': [
                'matplotlib.figure'
                #'sqlalchemy.util.queue',
                #'scipy.linalg.cython_blas',
                #'scipy.linalg.cython_lapack',
                #'scipy.special._ufuncs_cxx'
            ]
        }},
    data_files=DATA
)