Spring 2015 Team Emails:
Jordan Vaa: smewhen@gmail.com
Courtney Duquette: courtney.duquette.12@cnu.edu
Ashna Aggarwal: aaggarwal01@email.wm.edu
----------------------------------------------------------------------------------------------------
CALIPSO_Visualization_Tool.PY:
	Imports Required:
		TKINTER - import - Tk, Label, Toplevel, Menu, Text, END, PanedWindow, Frame, TOP, Button, IntVar, HORIZONTAL,
    			RAISED, BOTH, VERTICAL, Menubutton, Message, Canvas, NW, Scrollbar, BOTTOM, RIGHT, LEFT, 
			X, Y, SUNKEN, ALL --> For all GUI
		TKFILEDIALOG --> File Load Dialog
		IMAGE and IMAGETK from PIL --> For displaying and manipulating images (Eclipse claims these are unresolved imports, but they still work)
		SYS --> For inter-python scrypt communication
		bokeh.colors - import - white --> For background color white
	

	Class: CALIPSO
		Attributes:
			root --> the parent TK
			file --> name of the .hdf file to be plotted
			zoomvalue --> arbitrary value denoting zoom magnitude
			imageFilename --> name of the .png file created as the plot
		
		Top-Level Widgets
			fileDialog --> Label that holds the string representing 'file'			
			lowerLabel --> Label that the main image is saved
			m1 --> The base Paned Window that contains the other paned Windows. Stretches the paned to fit the whole window 
			m2 --> The Paned Window that splits the window into a top and bottom section 
			frmTop --> Frame that holds the buttons and file dialog
			frmBottom --> Frame that colds the canvas object upon which the plots and default image are displayed
			pndwintop --> The Paned window that the upper frame sits on where the buttons are
			pndwinbottom --> The Paned Window that contains the canvas.
			canvasLower --> Canvas that holds the default image as well as the plots
			xscrollbar --> Scrollbar for scrolling up and down
			yscrollbar --> Scrollbar for scrolling side to side			
			
		Class Methods:
				__init__(self, r) --> Initializes class variables, sets up basic containers for main screen[The paned-windows, canvas on which the images are displaeyd], as well as the scroll bars.
			## Main Window Setup
				centerWindow() --> centers the GUI on the screen
				*setupWindow() --> initializes all the various aspects of the GUI. Specifically calls setupMenu() and setupMainScreen()
			  
			## Menu Bar
				importFile() --> Creates a new window containing the load file dialog
				exportImage() --> N/A
				saveImage() -->N/A
				saveAs() --> N/A
				about() --> Creates a new window which displays information about the tool
				tutorial() --> Creates a new window which displays a short dialog 
				*setupMenu() --> initializes the file menu and the help menu
			  
			## Main Screen
				addToCanvas --> Accepts a PhotoImage and creates it on the canvasLower object
				loadPic() --> Finds an image object based on a given path, and loads it to addToCanvas
				selPlot() --> Determines which plot type was selected, and attempts to create that plot image
				zoomIn() --> Increases zoomvalue by 1, then multiplies the dimensions of the image by an arbitrary amount and the zoom value.
					The images dimensions are then increased by this value, and the new image then replaces the smaller image.
				zoomOut() --> The zoomvalue is evaluated to ensure that it does not equal 0. If zoomvalue is 0, no action is taken and the function terminates. 
					If zoomvalue does not, it is reduced by one. The images dimensions are then reduced by an arbitrary amount, equal to that of the increase on zoom in, and the zoom value.
					The current image is then replaced with the new image.
				reset() --> The filename is cleared, and the plot is replaced with the default image of the A train.
				polygon() --> N/A
				freeDraw() --> N/A
				topPanedWindow() --> Container that holds the the file dialog box, the buttons, and the plot selection radio-buttons.
				*setupMainScreen() --> Method that sets the canvas to default image, calls topPanedWindow().
				
*Call from "__main__" (public methods)
----------------------------------------------------------------------------------------------------
Setting Up the Environment: 
	- Download Python Anaconda 2.7
		- To install numpy: Open command window, navigate to the Anaconda directory and type "conda install numpy", "y" , "exit"
	- CCPLOT
		- Install Basemap
			- https://code.google.com/p/pythonxy/wiki/AdditionalPlugins 
			- Execute basemap-1.0.2_py27.exe
			- Destination directory: \Anaconda\Lib\site-packages\basemap
		- Install CCPLOT
			- Get http://sourceforge.net/projects/ccplot/files/ccplot/ccplot-1.5-rc7.win32-py2.7.exe from http://ccplot.org/ 
			- Run ccplot-1.5-rc7.win32-py2.7.exe
			- Browse to Anaconda install directory and install in \Anaconda\Lib\site-packages\ 
			- More information is at http://ccplot.org/ 
	- Eclipse Luna
		- Once Eclipse is installed and running
		- Within Eclipse, go to "Help" --> "Install New Software" --> input PyDev Website (http://pydev.org/updates) 
		- Under "Windows" --> "Preferences" --> "PyDev" --> "Interpretors" --> "Python" --> "Advanced Auto-Config" or manually find Anaconda
		- Import existing "CALIPSO_Visualizer" package
----------------------------------------------------------------------------------------------------
To Do:
	- Complete and test
		- Save Image/Save As Functions
		- Polygon/Free Draw Functions
			- Utilizing MATPLOTLIB functions
		- Exporting Functions
	- Set up Tutorial Function
	- Determine which functions/variables above should be private and which should be public
	- Streamline method of adding new plot types
	- Add native ccplot functionality 
		- including ability to manipulate the production of plots to a finer extent than current
		- Make axes customizable
	- Zoom in on users choice of location, not arbitrarily in the corner
	- Tie scroll to the scroll wheel.
	- Make the zoom window be only on the plot, not title, axes, and color-map
	- Make .png files delete upon exiting GUI
	- Have multiple files being saved for the user to flip between within the code
Think about:
	- Drawing plot inside of GUI, not importing plot as image
		- This would allow for enhanced zooming, as well as easier selection process
	- Creating .exe and .app executables alongside installation modules
		- ease of use and access
	