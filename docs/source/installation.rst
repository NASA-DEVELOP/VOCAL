============
Installation
============

VOCAL is still in it's early stages of development, and does not yet offer an in-depth
installer. As a result running VOCAL requires you to setup the development environment,
which can be tricky for those not well versed in programming. We've tried to be as
descriptive as possible in our installation guide for both Windows [#f1]_ , Linux and Mac
users. If you have any questions or trouble installing VOCAL, feel free to ask for help
from the :doc:`support page <trouble/contact>` and describe your issue to us.

.. toctree::
   :maxdepth: 1

   packages

.. note:: 

   Please read our :doc:`developer documentation <dev/startdev>` before developing yourself!

****************
Windows [#f1]_
****************

1. Download Python Anaconda 2.7

2. Open a terminal, navigate to the Anaconda installation directory and type
   ``conda install numpy`` , ``y``

3. Grab the *basemap* package ``conda install basemap``, ``y``

4. Install PIL ``conda install pillow``, ``y``

   * PIL is an old library and can often cause some errors, if when running
     VOCAL you receive the error ``Import Error: cannot import name _imagingtk``,
     see the :doc:`FAQ <trouble/faq>` on fixing this error

5. To install CCPLOT:

   * get `ccplot-1.5-rc7.win32-py2.7.exe`_
   * run ``ccplot-1.5-rc7.win32-py2.7.exe``
   * browse to the Anaconda install directory and install in ``\Anaconda\Lib\site-packages\``
   * more information is at http://ccplot.org/

6. Optional:

   * If using Eclipse [#f2]_ :, then once Eclipse is installed and running

      * within Eclipse, go to *help* --> *Install New Software*

        * input PyDev Website (http://pydev.org/updates)

      * under *Windows* --> *Preferences* --> *PyDev* --> *Interpreters* --> *Python*

        * "Advanced Auto Config" or manually find Anaconda

      * import the existing "CALIPSO_Visualizer" package under the ``file`` menu

   * If using PyCharm : Simply set the python interpreter to the one supplied by anaconda.

7. Download the zip from the GitHub or use Git (see `cloning the repository <dev/startdev#Clone-the-Repository>`)

8. Using command prompt or bash, :bash:`cd` into the *VOCAL/calipso* folder and use :bash:`python Calipso.py`

   * If using Eclipse or Pycharm, use their built-in tools to clone the repository from GitHub


************
Linux [#f3]_
************

.. note::
   At this time, Linux and OS X have not been tested with the current version of VOCAL. Installation
   may not work

1. start off by grabbing the SciPy Stack
  
   * ``sudo apt-get install python-numpy python-scipy python-matplotlib``

2. install basemap

   * ``sudo apt-get install python-mpltoolkits.basemap``

3. installing CCPLOT

   * CCPLOT has quite a bit of dependencies, so run

     * ``sudo apt-get install --no-intall-recommends cython libhdf4-dev libhdfeos-dev python-imaging ttf-bitstream-vera``

   * now CCPLOT needs to be built on Linux, so grab the `source`_
   * extract the source anywhere you'd like, the directory does not matter
   * ``cd`` into the CCPLOT folder you just extracted
   * run ``python setup.py build``
   * *note* if python cannot find ``HdfEosDef.h``

     * run ``dpkg -L``
     * search for the location of ``HdfEosDef.h``, it is commonly found in ``usr/include/x86_64-linux-gnu/hdf/``
     * open ``setup.py`` in the CCPLOT folder, and change line 24 to include your path
     * the new line would like similar to ``hdf_include_dirs = ['/usr/include/x86_64-linux-gnu/hdf', '/usr/include/hdf', '/usr/local/include/hdf/', '/opt/local/include']``
     * rerun ``python setup.py build``

   * run ``python setup.py install`` , ``sudo`` may be required as well
   * CCPLOT should be installed

4. install bokeh.color

   * ``sudo pip install bokeh``

5. run the application with ``python CALIPSO_Visualization_Tool.py``

***********
OS X [#f4]_
***********

1. install XCode

   * if using OS 10.9, install xcode 6.2

2. install macport

   * if *port* command not found in terminal, edit paths by

      * ``sudo vi /etc/paths``
      * add the following lines:

         * ``/opt/local/bin``
         * ``/opt/local/sbin``

      * restart terminal

   * do ``port selfupdate``

      * if you receive the error *'rsync: failed to connect to <address> : connection
        refused (61) ...'*

         * it is likely your firewall is preventing access to the address `ref`__
         * navigate to */opt/local/etc/macports* in your terminal
         * open *sources.config* with admin access ``sudo vim sources.conf``
         * comment out the **last** line, replace it with
           ``https://distfiles.macports.org/ports.tar.gz [default]`` `ref`__
         * run ``port -v -d sync``
         * run ``port search hdf4``
         * you should have queries show up, meaning ports it working!
3. run ``sudo port install hdf4 hdfeos py27-cython py27-numpy py27-matplotlib
   py27-matplotlib-basemap``

4. as root, do the following commands

   * ``mv /usr/bin/python /usr/bin/python.orig``
   * ``ln -s /opt/local/bin/python /usr/bin/python``

   * run ``port select --set python python27``
5. download *ccplot-1.5.tar.gz* from `here`_

   * run ``tar xzf ccplot-1.5.tar.gz``
   * ``cd ccplot-1.5.tar.gz``
   * ``python setup.py build``
   * ``python setup.py install --user``
   * ``ccplot -v``
   * and ccplot should be a recgonizable command!

6. Install bokeh ``port install py27-bokeh``

7. Install sqlalchemy ``port install py27-sqlalchemy``

8. download the IDE of your choice, or run ``python Calipso.py``

.. _basemap package: https://code.google.com/p/pythonxy/wiki/AdditionalPlugins

.. _ccplot-1.5-rc7.win32-py2.7.exe: http://sourceforge.net/projects/ccplot/files/ccplot/ccplot-1.5-rc7.win32-py2.7.exe

.. _source: https://sourceforge.net/projects/ccplot/files/ccplot/ccplot-1.5.tar.gz/download

.. _here: http://sourceforge.net/projects/ccplot/files/ccplot/ccplot-1.5.tar.gz/download

.. __: https://trac.macports.org/wiki/FAQ#selfupdatefails

.. __: https://trac.macports.org/wiki/howto/PortTreeTarball

.. rubric:: Footnotes

.. [#f1] x86 (32bit) is currently the only supported architecture for windows
.. [#f2] Eclipse is not mandatory, and not recommended over PyCharm, but can be used to develop
.. [#f3] The packages specified in the instructions may not be comprehensive, if additional packages are required please inform the team so they can correctly add them to the docs
.. [#f4] Tested on OS X 9.5


