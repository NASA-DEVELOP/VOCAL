#===============================================================================
# 
# Created on Jul 16, 2015
# 
# @author: nqian, Grant Mercer
# 
#===============================================================================
from setuptools import setup, find_packages

setup(name='vocal',
      version='0.15.2.b',
      description='A data visualization tool for viewing CALIPSO data and sharing features of data',
      author='Grant Mercer, Nathan Qian',
      url='https://github.com/syntaf/vocal',
      download_url='https://github.com/Syntaf/travis-sphinx/archive/master.zip',
      keywords=['scientific, visualization, nasa, tool'],
      packages = find_packages(),
      entry_points = {
          'console_scripts' : ['vocal=calipso.Calipso:main']
      },
      install_requires=[
          'matplotlib',
          'PIL',
          'bokeh',
          'numpy',
          'sqlalchemy',
          'ccplot'
      ],
      classifiers = ['Topic :: Software Development :: Data Visualization',
                     'Programming Language :: Python']
    )
