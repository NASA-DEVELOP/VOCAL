CALIPSO_Visualization_Tool.PY:
------------------------------------

Visualization software

###### Imports Required:

| Package | Imports |
| :-----: | :------ |
|TKinter  | `Tk`,`Label`,`Toplevel`,`Menu`,`Text`,`END`,`PanedWindow`,`Frame`,`TOP`,`Button`,`IntVar`,`HORIZONTAL`  |
|         | `RAISED`,`BOTH`,`VERTICAL`,`Menubutton`,`Message`,`Canvas``NW`,`Scrollbar`,`BOTTOM`,`RIGHT`,`LEFT`,`X` |
|         | `Y`,`SUNKEN`,`ALL`		                                                                            |
| tkFileDialog | `File`,`Load`,`Dialog` |
| PIL     | `Image`,`ImageTk`           |
| sys     |                             |
| bokeh.colors | `white`                |
	
## Class Breakdown:
* ###CALIPSO
  * ####Attributes:
    * **root** `............` the parent TK
    * **file** `..............` name of the .hdf file to be plotted
    * **zoomvalue** `.......` arbitrary value denoting zoom magnitude
    * **imageFilename** `...` name of the .png file created as the plot
	
  * ####Top-Level Widget
    * **fileDialog** `.......` Label that holds the string representing 'file'		
    * **lowerLabel** ` .....` Label that the main image is saved
    * **basepane** `............` Base Paned Window conaining other paned Windows. Stretches to fit whole window 
    * **sectionedpane** `............` The Paned Window that splits the window into a top and bottom section 
    * **buttonFrame** `........` Frame that holds the buttons and file dialog
    * **drawplotFrame** `.....` Frame holds the canvas object upon which the plots/default image are displayed
    * **pndwintop** `.....` The Paned window that the upper frame sits on where the buttons are
    * **pndwinbottom** `.` The Paned Window that contains the canvas.
    * **drawplotCanvas** `..` Canvas that holds the default image as well as the plots
    * **xscrollbar** `.....` Scrollbar for scrolling up and down
    * **yscrollbar** `.....` Scrollbar for scrolling side to side			
		
  * ####Methods:
    * **\_\_init\_\_(*self*, r) :**
      * Initializes class variables, sets up basic containers for main screen[The paned-windows, canvas on which the        images are displaeyd], as well as the scroll bars.
		
  * ####Main Window Setup
      * **centerWindow()** : 
        * centers the GUI on the screen
      * **\*setupWindow()** : 
        * initializes all the various aspects of the GUI. Specifically calls setupMenu() and setupMainScreen()
		  
  * ####Menu Bar
    * **importFile()** : 
      * Creates a new window containing the load file dialog
    * **exportImage()** : 
    * **saveImage()** :
    * **saveAs()** :
    * **about()** : 
      * Creates a new window which displays information about the tool
    * **tutorial()** : 
      * Creates a new window which displays a short dialog 
    * **\*setupMenu()** : 
      * initializes the file menu and the help menu
			  
  * ####Main Screen
    * **addToCanvas** :
      * Accepts a PhotoImage and creates it on the canvasLower object
    * **loadPic()** :
      * Finds an image object based on a given path, and loads it to addToCanvas
    * **selPlot()** :
      * Determines which plot type was selected, and attempts to create that plot image
    * **zoomIn()** :
      * Increases zoomvalue by 1, then multiplies the dimensions of the image by an arbitrary amount and the zoom value. The images dimensions are then increased by this value, and the new image then replaces the smaller image.
    * **zoomOut()** :
      * The zoomvalue is evaluated to ensure that it does not equal 0. If zoomvalue is 0, no action is taken and the function terminates. If zoomvalue does not, it is reduced by one. The images dimensions are then reduced by an arbitrary amount, equal to that of the increase on zoom in, and the zoom value. The current image is then replaced with the new image.
    * **reset()** :
      * The filename is cleared, and the plot is replaced with the default image of the A train.
    * **polygon()** :
    * **freeDraw()** :
    * **topPanedWindow()** : 
      * Container that holds the the file dialog box, the buttons, and the plot selection radio-buttons.
    * **\*setupMainScreen()** : 
      * Method that sets the canvas to default image, calls topPanedWindow().
				

`*Call from "__main__" (public methods)`


## Setting Up the Environment: 

###### Windows:

1. Download Python Anaconda 2.7
2. numpy: To install numpy, open command window, navigate to the Anaconda directory and type 
  * `conda install numpy`, `y` , `exit`
3. To Install Basemap:
  * https://code.google.com/p/pythonxy/wiki/AdditionalPlugins 
  * Execute basemap-1.0.2_py27.exe
  * Destination directory: \Anaconda\Lib\site-packages\basemap
4. To Install CCPLOT:
  * Get http://sourceforge.net/projects/ccplot/files/ccplot/ccplot-1.5-rc7.win32-py2.7.exe from http://ccplot.org/ 
  * Run ccplot-1.5-rc7.win32-py2.7.exe
  * Browse to Anaconda install directory and install in \Anaconda\Lib\site-packages\ 
  * More information is at http://ccplot.org/ 
5. Install Eclipse Luna, Then:
  * Once Eclipse is installed and running
  * Within Eclipse, go to "Help" --> "Install New Software"
    * input PyDev Website (http://pydev.org/updates) 
  * Under "Windows" --> "Preferences" --> "PyDev" --> "Interpretors" --> "Python"
    * "Advanced Auto-Config" or manually find Anaconda
6. Import existing "CALIPSO_Visualizer" package

###### Linux:

1. Start off by grabbing the SciPy Stack
  * `sudo apt-get install python-numpy python-scipy python-matplotlib`
2. Install Basemap
  * `sudo apt-get install python-mpltoolkits.basemap`
3. Installing CCPLOT
  * CCPLOT has quite a bit of dependencies, so run
    * `sudo apt-get install --no-intall-recommends cython libhdf4-dev libhdfeos-dev python-imaging ttf-bitstream-vera`
  * Now CCPLOT must be built yourself, so first grab the [source](https://sourceforge.net/projects/ccplot/files/ccplot/ccplot-1.5.tar.gz/download)
  * Extarct the source anywhere you'd like, the directory does not matter
  * `cd` into the CCPLOT folder
  * run `python setup.py build`
  * *note* if python cannot find `HdfEosDef.h`
    *  run `dpkg -L`
    *  search for the location of `HdfEosDef.h`, in my case it was located in `usr/include/x86_64-linux-gnu/hdf/`
    *  open `setup.py` in the CCPLOT folder, and change line 24 to include your path
    *  the new line would look like `hdf_include_dirs = ['/usr/include/x86_64-linux-gnu/hdf', '/usr/include/hdf', '/usr/local/include/hdf/', '/opt/local/include']
    *  rerun `python setup.py build` with the new modification
  * run `sudo python setup.py install`
  * now CCPLOT should be installed. You can also view [CCPLOTs installation instructions](http://ccplot.org/download/)
4. Install bokeh.color
  * `sudo pip install bokeh`
5. Run the application with `python CALIPSO_Visualization_Tool.py`


###### To Do:

- [ ] Complete and test
  - [ ] Save Image/Save As Functions
  - [ ] Polygon/Free Draw Functions
    - [ ] Utilizing MATPLOTLIB functions
  - [ ] Exporting Functions
- [ ] Set up Tutorial Function
- [ ] Determine which functions/variables above should be private and which should be public
- [ ] Streamline method of adding new plot types
- [ ] Add native ccplot functionality 
  - [ ] including ability to manipulate the production of plots to a finer extent than current
  - [ ] Make axes customizable
- [ ] Zoom in on users choice of location, not arbitrarily in the corner
- [ ] Tie scroll to the scroll wheel.
- [ ] Make the zoom window be only on the plot, not title, axes, and color-map
- [ ] Make .png files delete upon exiting GUI
- [ ] Have multiple files being saved for the user to flip between within the code

###### Think about:

- Drawing plot inside of GUI, not importing plot as image
  - This would allow for enhanced zooming, as well as easier selection process
- Creating .exe and .app executables alongside installation modules
  - ease of use and access

###### Spring 2015 Team Emails:
- Jordan Vaa: smewhen@gmail.com
- Courtney Duquette: courtney.duquette.12@cnu.edu
- Ashna Aggarwal: aaggarwal01@email.wm.edu
