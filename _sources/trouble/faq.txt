============
Troubleshoot
============
::

> how do I actually run this project?

  The main is included in ``Calipso.py``, once you've followed the installation instructions run it through either eclipse or ``python Calipso.py``

::

> when I try to run the project I get the error:
> ImportError:  cannot import name _imagingtk

  First, ensure you do not have PIL installed alongside Pillow. These two packages can not coexist and will likely cause issues if you have both installed.

  If that is not the case, for Linux users try running ``sudo apt-get install python-imaging-tk`` . Windows users need to take a couple extra steps

  * Remove any related packages on conda, ``conda remove PIL`` or ``conda remove Pilow``
  * Install ``PIL`` from `here`_ , ``PIL-1.1.7.win32-py2.7.exe``

::

> ccplot's setup.py build cannot find HdfEosDef.h

  This is an error due to the setup.py script not being comprehensive, the solution is covered in the :doc:`../installation` instructions for Linux. You can also read about why you get this issue on the github bug tracker for ccplot `here[1]`_

::

> running 'port selfupdate' gives me error about the connection being refused

  Your firewall is likely blocked, see the :doc:`OS X installations instructions <../installation>` for further information

::

> ccplot can't seem to find the package basemap, but I already installed it

  The problem is that your python path is probably set to the default python supplied by OS X,
  but you want to use the python supplied by macports. To do this see the :doc:`OS X installations instructions <../installation>`

::

> while importing PIL on windows, Eclipse tells me Image
> and ImageTk are unresolved

  This is a known issue, and unless you are actually receiving errors this can be ignored

.. _here: http://www.pythonware.com/products/pil/
.. _here[1]: https://github.com/peterkuma/ccplot/issues/1
