==========================
Coding Conventions
==========================

Below is list of coding conventions agreed upon by Nathan and I(Grant). Please adhere to these conventions to create a more readable codebase.

.. rubric:: Variables

Variables should be in the ``camelCase`` format in all cases.::

    var = 3
    anotherVar = 4
    moreWordsThanPreviousVar = 5

.. rubric:: Functions

The same format as Variables, ``camelCase`` should be used.::

    def func():

    def adheresToCodingConventionFunc():

.. rubric:: Classes

Uppercase ``CamelCase`` should be used to repesent classes.::

    class Shape(object):

    class SquareObject(Shape):

.. rubric:: Tabs

Currently CALIPSO uses tabs instead of spaces.::

    var = [1,2,3,4,5]
    for v in var:
        print v        # tab should be 4 spaces long

.. rubric:: General Rules

No spaces should be left between conditional statements and loops code blocks.::

    if x is not y:
        # ...

    for x in y:
        # ...

Comments should be right justified when applicable, and only above lines when necessary to explain a section of code(not just one line).::

    var = x - y + r*2           # calculate ___ and place in var
    doFunc(var)                 # do some func with var param
    if var[-1] is not var[:3]:      
        err()                   # error is var does not match criteria

    # Set the value of var and pass var into a set of functions which calculate things based off var
    var = x - y + r*2
    doAllFuncs(var)
    


