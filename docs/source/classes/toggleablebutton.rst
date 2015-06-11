==================
ToggleableButton
==================

A Class which wraps the Tkinter Button object and simulates the toggled button you commonly see in draw, magnify, etc. buttons. Keeps a static container of toggleable buttons to only allow one button at any time to be toggled.

.. py:module:: tools

.. py:class:: ToggleableButton(Button, object)

   .. py:data:: self.__bindMap

      bind map consisting of a list of tuples containing a key and function to bind to that key. bindMap is iterated over and sets the keys accordingly during a toggle

   .. py:data:: self.isToggled

      internal var to keep track of toggling

   .. py:data:: self.__root

      copy of ``root`` for use with changing cursor

   .. py:data:: self.__destructor

      desctructor called after the button is 'untoggled' and the keys are unbound

   .. py:data:: self.__master

      widget to draw the button to

   .. py:method:: __init__(self, root, master=None, cnf={}, **kw)
      :noindex: 

      Creates button and binds command to internal function :py:meth:`Toggle`  

      :param Widget root: The root of the program, or global cursor handle
      :param Widget master: Location the button will be packed to
      :param cnf: Button forwarded args
      :param kw: Button forwarded args

   .. py:method:: latch(self, key="", command=None, cursor="", destructor=None)
      :noindex:

      Binds a *key* to a *command* upon the button being toggled, stored inside a bindmap. **Note** latch is additive, it can be called multiple times to bind multiple keys

      :param str key: A valid Tkinter command key
      :param func command: The function to be binded to the key
      :param str cursor: a valid Tkinter cursor to be set upon toggle
      :param func destructor: A function called upon un-toggling the button
      
   .. py:method:: unToggle(self)
      :noindex:

      Manually untoggle the button

   .. py:method:: Toggle(self)
      :noindex:

      The method bound to the button, *Toggle* will internally bind the inputed keys when toggled, and unbind them accordingly. Also keeps track of all toggled button via a static container and ensures only one button can be toggled at any time
