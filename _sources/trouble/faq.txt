========================
Troubleshoot
========================
::

> How do I actually run this project?

  The main is included in ``Calipso.py``, once you've followed the installation instructions run it through either eclipse or ``python Calipso.py``

::

> When I try to run the project I get the error: 
> ImportError:  cannot import name _imagingtk

  First, ensure you do not have PIL installed alongside Pillow. These two packages can not coexist and will likely cause issues if you have both installed.

  If that is not the case, for Linux users try running sudo apt-get install python-imaging-tk . Windows users need to take a couple extra steps

  * Remove any related packages on conda, ``conda remove PIL`` or ``conda remove Pilow``
  * Install ``PIL`` from `here`_ , ``PIL-1.1.7.win32-py2.7.exe``

::

> ccplot's setup.py build cannot find HdfEosDef.h

  This is an error due to the setup.py script not being comprehensive, the solution is covered in the :doc:`../installation` instructions for Linux. You can also read about why you get this issue on the github bug tracker for ccplot `here[1]`_

.. _here: http://www.pythonware.com/products/pil/
.. _here[1]: https://github.com/peterkuma/ccplot/issues/1

::

> While importing PIL on windows, Eclipse tells me Image
> and ImageTk are unresolved

  This is a known issue, and unless you are actually receiving errors this can be ignored
