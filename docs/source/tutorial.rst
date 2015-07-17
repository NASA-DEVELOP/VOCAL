===============
Getting Started
===============

This tutorial provides an overview on how to use the CALIPSO Visualization 
Tool program.

-----------
Main Screen
-----------

The CALIPSO Visualization Tool window is the main screen for displaying 
CALIPSO data and shapes. The menu bar provides access to the shape database 
and loading CAlIPSO hdf files. The Visualization Tool window is accompanied by
a toolwindow that contains buttons for manipulating the main screen, drawing 
shapes, and saving and loading shapes. 
 
.. image:: _static/startup.png
   :scale: 40%
       
-----------
Starting Up
-----------

To load a CALIPSO hdf file from the local file directory, click the |browse| button at the
top of the screen. Navigate to the .HDF file of your choice and select **open** The file text box will now update and
display the name of the imported hdf file. The main screen will appear blank at first. To display a plot,
Select the type of plot you would like to render and an optional step (*the default is from 0 to 1000*).
Hit **Render** to visualize the data to the screen.
 
.. image:: _static/load_hdf.png
   :scale: 60%
 	   
-------------------
Navigating the Plot
-------------------

The first row of toolbar buttons allows you to manipulate the plot for the purpose of drawing.

* |move| Pan: Clicking and dragging will allow you to move the plot across
  the screen by the amount of drag used, either left or right.
* |magn| Magnify: Selecting this
  button will allow you to zoom in and out of the plot. To zoom in, click and
  drag with the left mouse button the area on the plot you wish to zoom in. To
  zoom out, click and drag with the right mouse button and the plot will zoom
  out based upon the scale difference of the area you highlighted.
* |undo| Undo: jump to the previous magnification zoom frame
* |redo| Redo: jump forward to the next magnification zoom frame
* |home| Home: reset the view to the original render

-------------------------------------------
Extracting and Viewing Attributes of Shapes
-------------------------------------------

The second row of buttons (minus the home button) is dedicated to the viewing, assigning, and
extraction of data from shapes

* |prop| Properties: Clicking on a shape while the properties button is active will open a small
  window detailing the range of time and altitude covered by the shape, attributes, and notes.
  click once more to hide the properties window
* |attr| Attributes: Clicking on a shape while the attributes button is active will open a
  dialog window for assigning attributes to shapes. Attributes on the **left** are the *available*
  attributes, the **right** side is the *selected* attributes. Add any notes you wish and click
  ``save`` to save the notes and attributes. These can be viewed with |prop|
* |extr| Extract: Clicking on a shape while the extract button is active will create a subplot
  containing only the data enclosed in the shape. Future features are to come but for now a
  subplot and histogram are generated for the shape.

--------------
Drawing Shapes
--------------

The third row of buttons is for creating and manipulating the physical properties of
shapes drawn to the plot.

* |rect| Rectangle: Dragging the cursor in the plot will create an outline of a rectangle,
  upon release of the cursor the shape will be created in place of the outline.
* |fred| Free Draw: Clicking on the plot will create a *vertex*, multiple clicks will
  bind vertices together and create lines. If a new line is found interesting an
  existing line a shape will be formed at the intersection being the enclosing vertex.
* |eras| Erase: Selecting this button and clicking a shape will remove it from the plot. *note: *
  this will **not** delete the object in a database or JSON file if it is loaded, that is a
  separate deletion itself
* |pain| Paint: Give a shape a new color value by selecting either a predefined color or
  some custom value on the color wheel. Changing the color of a shape will not create
  a new shape, simply update the color value of existing shapes you've loaded.

---------------------------
Hiding and Exporting Shapes
---------------------------

The last row of buttons deals with global state of shape viewing as well as the exporting
of shapes to a JSON file.

* |focs| Focus: Press this button to display all shapes *and* future shapes as unfilled.
  Only the outline of the shapes will be drawn, pressing this one more reverts the change
* |hide| Hide: Similar to Focus, but pressing this button will **completely** hide all shapes,
  they still exist; however they simply won't be drawn to the screen.
* |save| Save: Save all existing objects in the **current** plot to a ``JSON`` formatted file.
  These objects can be loaded back into the screen with the next button and can be shared
  between researchers that wish to personally hand over shapes to another user for loading. If
  you wish to save all shapes from **every** plot into one fill, these is a ``save all`` option
  in the file menu for this.
* |load| Load: Given a valid ``.JSON`` file, load all polygon objects present in the file and
  display them to the plot.


------------------
Using the Database
------------------

The CALIPSO Visualization Tool has access to a database that can save shapes,
so that other users can share the shapes they have drawn. To save shapes to 
the database, click on "Polygon" from the menu bar and select "Export to
Database." The program will take each individual shape drawn on each plot and 
saves each shape independently in the database. To import shapes from the 
database, click on "Polygon" from the menu bar and select "Import from 
Database." A dialog box will appear, displaying all the shapes saved on the 
database. To help find specific shapes, you can sort name, plot, date, file,
attributes, and notes by clicking on the header bar. To search specifically 
within the attributes, use the search bar at the top of the dialog to filter 
shapes. To select an individual shape, simply click on an entry. For multiple
entries, hold the Control button on the keyboard while clicking on entries. To
retrieve successive entries, hold the Shift button on the keyboard while 
selecting a start and end entry. To delete the selected entries click on the 
"Delete" button at the top right of the window. If you wish to import these
shapes, click on the "Import" button at the bottom of the window, and the plot
will automatically draw all the loaded shapes.


.. |browse| image:: _static/browse_button.png
.. |move| image:: _static/move_button.png
.. |magn| image:: _static/magnify_button.png
.. |undo| image:: _static/undo_button.png
.. |redo| image:: _static/redo_button.png
.. |home| image:: _static/home_button.png
.. |prop| image:: _static/properties_button.png
.. |attr| image:: _static/attributes_button.png
.. |extr| image:: _static/extract_button.png
.. |rect| image:: _static/rect_button.png
.. |fred| image:: _static/freedraw_button.png
.. |eras| image:: _static/erase_button.png
.. |pain| image:: _static/paint_button.png
.. |focs| image:: _static/focus_button.png
.. |hide| image:: _static/hide_button.png
.. |save| image:: _static/save_button.png
.. |load| image:: _static/load_button.png
