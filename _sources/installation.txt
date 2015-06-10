====================
Installation
====================

Installation guide for both Windows [#f1]_ and Linux users

*********************
Windows [#f1]_
*********************

1. Download Python Anaconda 2.7
2. Open a terminal, navigate to the Anaconda installation directory and type ``conda install numpy``, ``y``, ``exit``
3. Grab the `basemap package`_
  
   * Execute ``basemap-1.0.2_py27.exe``
   * The destination directory is ``\Anaconda\Lib\site-packages\basemap``

4. To install CCPLOT:

   * Get `ccplot-1.5-rc7.win32-py2.7.exe`_
   * Run ``ccplot-1.5-rc7.win32-py2.7.exe``
   * Browse to the Anaconda install directory and install in ``\Anaconda\Lib\site-packages\``
   * More information is at http://ccplot.org/

5. Install Eclipse Luna [#f2]_ , then once Eclipse is installed and running

   * Within Eclipse, go to *help* --> *Install New Software*

     * Input PyDev Website (http://pydev.org/updates)

   * Under *Windws* --> *Preferences* --> *PyDev* --> *Interpreters* --> *Python*

     * "Advanced Auto Config" or manually find Anaconda

6. Import the existing "CALIPSO_Visualizer" package under the ``file`` menu

*********************
Linux [#f3]_
*********************

1. Start off by grabbing the SciPy Stack
  
   * ``sudo apt-get install python-numpy python-scipy python-matplotlib``

2. Install basemap

   * ``sudo apt-get install python-mpltoolkits.basemap``

3. Installing CCPLOT

   * CCPLOT has quite a bit of dependencies, so run

     * ``sudo apt-get install --no-intall-recommends cython libhdf4-dev libhdfeos-dev python-imaging ttf-bitstream-vera``

   * Now CCPLOT needs to be built on Linux, so grab the `source`_
   * Extract the source anywhere you'd like, the directory does not matter
   * ``cd`` into the CCPLOT folder you just extracted
   * Run ``python setup.py build``
   * *Note* if python cannot find ``HdfEosDef.h``

     * Run ``dpkg -L``
     * Search for the location of ``HdfEosDef.h``, it is commonly found in ``usr/include/x86_64-linux-gnu/hdf/``
     * Open ``setup.py`` in the CCPLOT folder, and change line 24 to include your path
     * The new line would like similar to ``hdf_include_dirs = ['/usr/include/x86_64-linux-gnu/hdf', '/usr/include/hdf', '/usr/local/include/hdf/', '/opt/local/include']``
     * Rerun ``python setup.py build``

   * Run ``python setup.py install`` , ``sudo`` may be required as well
   * CCPLOT should be installed

4. Install bokeh.color

   * ``sudo pip install bokeh``

5. Run the application with ``python CALIPSO_Visualization_Tool.py``

.. _basemap package: https://code.google.com/p/pythonxy/wiki/AdditionalPlugins

.. _ccplot-1.5-rc7.win32-py2.7.exe: http://sourceforge.net/projects/ccplot/files/ccplot/ccplot-1.5-rc7.win32-py2.7.exe

.. _source: https://sourceforge.net/projects/ccplot/files/ccplot/ccplot-1.5.tar.gz/download

.. rubric:: Footnotes

.. [#f1] x86 (32bit) is currently the only supported architecture for windows
.. [#f2] Eclipse is not mandatory, but **highly** recommended
.. [#f3] The packages specified in the instructions may not be comprehensive, if additional packages are required please inform the team so they can correctly add them to the docs
