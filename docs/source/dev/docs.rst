=========================
Building and Writing Docs
=========================

One of the most important aspects of writing *good* software is clarity and readability.
We hope as other developers find themselves tasked with improving this tool, documentation
is also held to as high a standard as we do.

.. rubric:: Building the docs

See :doc:`Updating the Site <site>' for a guide on building docs for the website

.. rubric:: Contributing to the Docs

The CALIPSO docs page uses the ``sphinx.ext.autodoc`` extensions to pull reStructuredText
docstrings from source and create doc pages from them. inside the ``doc`` folder is the
location of all code documentation, split up into three packages: *general* , *polygon* ,
and *tools*. If you've created a new module and would like to have it added to the
docs(the answer should always be **yes**!), place a ``.rst`` file with the module name in
the corresponding package folder.

Lets run through the scenario you have a new module, ``foobar.py``, you wrote inside ``tools``.
It's recommended you don't procrastinate adding your new modules to the docs to avoid rushing.
Here's an example of what your file may look like, *note* the docstrings and the reStruct
markdown used

.. code-block:: python

   ########################
   #    foobar.py 
   #    04/07/2015
   #    @author: me
   ########################

   class Foo(object):
   """
   Manages certain functionality within the package, description of class utility

   :param str title: Title of window
   :param root: Root of application
   """

       def __init__(self, title, root):
           self.title = title
           self.root = root

       def does_stuff(self):
       """
       Does plenty of stuff

       :rtype: int
       """
           return 0

    def related_to_foo(foobar):
    """
    Takes a passed ``Foo`` object and does something with the object
    
    :param Foo foobar: A Foo object
    """
        # .....


Now when adding ``foobar.py``, you'll reference the package it is located in
(``tools`` in this case) and place a ``.rst`` file in the correct location.::

   > cd vocal
   > cd docs
   > cd doc
   > tree
   .
   |-- general
   |   |-- attributes.rst
   |   |-- calipso.rst
   |   |-- consts.rst
   |   |-- db.rst
   |   |-- general.rst
   |   |-- import.rst
   |   `-- toolswindow.rst
   |-- modules.rst
   |-- polygon
   |   |-- drawer.rst
   |   |-- list.rst
   |   |-- polygon.rst
   |   `-- reader.rst
   `-- tools
       |-- navigationtoolbar2calipso.rst
       |-- toggleablebutton.rst
       |-- tools.rst
       |-- tooltip.rst
       `-- treelistbox.rst
    > cd tools
    > vim foobar.rst

Inside ``foobar.rst`` simply specify the title and a couple auto doc lines.::

   ==============
   Foo
   ==============

   .. inheritance-diagram:: tools.foobar

   .. automodule:: tools.foobar
      :members:

The ``:members:`` specifier tells autodoc to also include the class methods, which we also want
to display.


And thats all! The documentation tool will create an inheritance diagram of all classes using
graphiz, then run through the module specified and document any classes or functions available.
Ensure you are using **docstrings** and are following the
:doc:`coding conventions </dev/conventions>`. If you ever run into problems not knowing how to
use sphinx, every doc page has a *view source* option you can refer to for help, and feel free
to contact us on the :doc:`contact page </trouble/contact>`.


.. _sphinx: http://sphinx-doc.org/
.. _graphviz: http://www.graphviz.org/
.. [#f1] You will likely need to add graphviz to your ``PATH`` once installed
