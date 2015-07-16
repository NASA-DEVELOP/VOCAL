=====================
Getting Started
=====================

This tutorial provides an overview on how to use the CALIPSO Visualization 
Tool program.

--------------------------------------------------
Main Screen
--------------------------------------------------

The CALIPSO Visualization Tool window is the main screen for displaying 
CALIPSO data and shapes. The menu bar provides access to the shape database 
and loading CAlIPSO hdf files. The Visualization Tool window is accompanied by
a toolwindow that contains buttons for manipulating the main screen, drawing 
shapes, and saving and loading shapes. 
 
.. image:: _static/startup.png
   :scale: 40%
       
--------------------------------------------------
Starting Up
--------------------------------------------------

To load a CALIPSO hdf file from the local file directory, click the |browse| button at the
top of the screen. Navigate to the .HDF file of your choice and select **open** The file text box will now update and
display the name of the imported hdf file. The main screen will appear blank at first. To display a plot,
Select the type of plot you would like to render and an optional step (*the default is from 0 to 1000*).
Hit **Render** to visualize the data to the screen.
 
.. image:: _static/load_hdf.png
   :scale: 60%
 	   
--------------------------------------------------
Plot Navigation
--------------------------------------------------

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

-------------------------------------------------
Shape Extraction and Viewing
-------------------------------------------------

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

--------------------------------------------------
Shape Drawing
--------------------------------------------------

The third row of buttons is for creating and manipulating the physical properties of
shapes drawn to the plot.

* |rect| Rectangle: Dragging the cursor in the plot will create an outline of a rectangle,
  upon release of the cursor the shape will be created in place of the outline.
* |fred| Free Draw: Clicking on the plot will create a *vertex*, multiple clicks will
  bind vertices together and create lines. If a new line is found interesting an
  existing line a shape will be formed at the intersection being the enclosing vertex.

The next seven buttons are used for shape drawing. The rectangle icon 
represents rectangle drawing. Pressing this button will allow you to draw 
rectangles. After pressing the button, click and drag with the left mouse 
button to draw a rectangle. The hand icon is the shape dragging button. When 
this button is selected, you can drag shapes by clicking and dragging with the
left mouse button. The pencil icon represents the free draw action. With this
action, you can draw polygon shapes. To draw a shape, click with the left 
mouse button to plot a point. Click again on a different spot to draw another 
point. After you plot the third point, if a line intersects with any 
previously drawn line, the plot will draw a shape based on the point of 
intersection. The last button in the row is the erase button, which allows 
you to delete shapes drawn on the plot. To delete a shape, simply click with 
the left mouse button the desired shape to be deleted.

In the third row, the button with overlapping rectangles is the toggle outline
button. When this button is pressed, all shapes drawn on the plot will only 
display their outlines. Pressing the button again will fill the shapes with 
solid colors. The next button is the paint button. To recolor a drawn shape, 
click with the left mouse button the desired shape. A dialog will prompt you 
to select which color to repaint the shape. The third button in the row is the
hide shapes button. Pressing this button will hide all shapes drawn on the 
plot. Clicking on the button again will make the shapes visible again.

--------------------------------------------------
Shape Saving and Loading
--------------------------------------------------

To save shapes draw on the plot, click on the button with the floppy disk 
image (third row, fourth button). If the shapes haven't been saved previously,
a file dialog will prompt you to save the shapes on your local file directory.
The shapes are saved as JavaScript Object Notation (JSON) files with the .json
file extension. If the shapes have been already saved, saving the shapes again
will automatically update the JSON file. To load the file, select the file 
with the folder icon (fourth row, first button). A file dialog will prompt you
to select one JSON file to import from your local file directory. The plot
will then draw the shapes according from the data saved in the JSON.

--------------------------------------------------
Importing and Exporting form the Database
--------------------------------------------------

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
