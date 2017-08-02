================
Vocal Data Block
================

.. inheritance-diagram:: tools.vocalDataBlock

This file was an attempt by a previous term to set up tabs in Tkinter to simultaneously load
multiple levels of data. After spending a lot of time trying to fix all of the problems with this
method, I realized I couldn't get any further and ended up replacing the tabs with a view menu,
which is a lot simpler and works much better. All of the fixes I made can be found in the
DataBlock branch on GitHub. I would NOT recommend retrying this method, however. I believe there
are some limitations from Tkinter and matplotlib/tkinter that would require vocal to be completely
restructured for simultaneous tabs to work.

Currently, this file simply serves to load both L1 and L2 files, although it may be prudent to
extract the method from VocalDataBlock.get_file_name(), place it in a separate file, and delete
this one

.. automodule:: tools.vocalDataBlock
   :members: