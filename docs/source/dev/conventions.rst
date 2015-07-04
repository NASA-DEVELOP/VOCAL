==========================
Coding Conventions
==========================

.. note::

   We are now using the ``pep-0008`` style guide as referenced `here`_ . See the link for a full list of conventions

Below is list of coding conventions agreed upon by Nathan and I(Grant). Please adhere to these conventions to create a more readable codebase.

.. rubric:: String Literals

String Literals are denoated with ``''``, docstring should be double quotes ``""``

.. code-block:: python

   var = 'Heres a string'
   def foo():
   """
   Heres a docstring
   """
       pass


.. rubric:: Variables

Variables should be lowercase and word separated with ``_`` 

.. code-block:: python

   var = 3
   another_var = 4
   more_words_than_previous_var = 5

.. rubric:: Functions

The same format as Variables, lowercase with ``_`` separating words should be used.

.. code-block:: python

   def func():
      # ...
   def adheres_to_coding_convention_func():
      # ...

.. rubric:: Classes

Uppercase ``CamelCase`` should be used to repesent classes.

.. code-block:: python

   class Shape(object):

   class SquareObject(Shape):

.. rubric:: Tabs

Currently should use spaces as opposed to tabs.::

    var = [1,2,3,4,5]
    for v in var:
        print v        # 4 space indent

.. rubric:: General Rules

No spaces should be left between conditional statements and loops code blocks.

.. code-block:: python

   if x is not y:
      # ...

   for x in y:
      # ...

Simple comments should be placed to the right of the line when possible, or one comment should be placed above a segment shortly explaning it's function

.. code-block:: python

   var = x - y + r*2           # calculate ___ and place in var
   doFunc(var)                 # do some func with var param
   if var[-1] is not var[:3]:      
      err()                   # error is var does not match criteria

   # does this and this and this
   var = x + 2
   x = var - 5
   if var == 0:
      err()


This documentation website is generated using docstrings from source, so **document** as you code! The docstring markdown is reStructedText Primer and sphinx, when the doc chain is generated it will use these docstrings from the code for the webpage. 

.. code-block:: python

   class Foo(object):
   """
   Class description is placed here

   :param <name>: description of param 'name'
   """
     
      def __init__(self, name):
         #...

      def foo(self, x, y)
      """
      Description of function here

      :param int x: parameter x is an integer and does ....
      :param int y: parameter y is an integer and does ....
      :rtype: returns int
      """

The auto documentation tool chain will generate this as:

.. py:class:: Foo
   :noindex:

   Class description is placed here

   :param name: description of param 'name'

   .. py:function:: foo(self, x, y)
      :noindex:

      Description of function here

      :param int x: parameter x is an integer and does...
      :param int y: parameter y is an integer and does...
      :rtype: returns int

If you are developing in an existing file , the doc chain *should* find your new function/class automatically. In the case you are creating a new module, determine whether it is in the ``general``, ``polygon`` or ``tools`` package, and create a ``.rst`` file in the corresponding doc/ folder specifying your new module. You can refer to the exisiting .rst files for how to populate the docs. You can also refer to the :doc:`Documentation Page </dev/docs>` for writing your own docs. 

.. _here: https://www.python.org/dev/peps/pep-0008/
