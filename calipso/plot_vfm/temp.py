"""
Demo of image that's been clipped by a circular patch.
"""
'''
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook

image_file = cbook.get_sample_data('grace_hopper.png')
image = plt.imread(image_file)

fig, ax = plt.subplots()
im = ax.imshow(image)
patch = patches.Circle((260, 200), radius=200, transform=ax.transData)
im.set_clip_path(patch)

plt.axis('off')
plt.show()
'''

from Tkinter import Label, Toplevel, Frame, Button, IntVar, \
   BOTH, BOTTOM, Radiobutton, Entry, TOP, Tk, X
   
CHILDWIDTH      = 200
CHILDHEIGHT     = 325

class ToolsWindow(Toplevel):

    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.__root = root
        self.plotType = IntVar()
        
        self.title("Tools")
        #self.geometry('%dx%d+%d+%d' % (CHILDWIDTH, CHILDHEIGHT,0, 0))
        #self.resizable(width=FALSE, height=FALSE)
        self.protocol("WM_DELETE_WINDOW", ToolsWindow.ignore)
        self.container = Frame(self, background="red")
        self.container.pack(side=TOP, fill=BOTH, expand=True )    
        
        self.coordinateFrame = Frame(self.container, background="green", width=50, height=50)
        self.coordinateFrame.config(highlightthickness=1)                        # create a small border around the frame
        self.coordinateFrame.config(highlightbackground="grey")
        self.coordinateFrame.pack(side=BOTTOM, fill=BOTH, expand=False)                                      
    
    @staticmethod
    def ignore():
        pass
        
    def setupToolBarButtons(self):
        self.upperButtonFrame = Frame(self.container, background="blue")                                  # upper button frame holding text buttons
        self.upperButtonFrame.pack(side=TOP, fill=X)    
        
        btnReset = Button(self.upperButtonFrame, text = "Reset", width = 12, command=self.render)
        btnReset.grid(row=0, column=0, sticky="w")
        btnRender = Button(self.upperButtonFrame, text = "Render", width = 9, command = self.render)
        btnRender.grid(row=0, column=1)
        
        self.bScattered = Radiobutton(self.upperButtonFrame, text="Backscattered", 
            variable=self.plotType, value=1).grid(row=1, column=0, sticky="w")
        self.depolarized = Radiobutton(self.upperButtonFrame, text="Depolarized", 
            variable=self.plotType, value=2).grid(row=2, column=0, sticky="w")

        self.upperRangeFrame = Frame(self.container, background="yellow")
        self.upperRangeFrame.pack(side=TOP, fill=X)

        self.rng = Label(self.upperRangeFrame, text="Step")
        self.rng.grid(row=3, column=0, sticky="w")
        self.e = Entry(self.upperRangeFrame, width=8)
        self.e.grid(row=3, column=1, sticky="w")
        
        self.to = Label(self.upperRangeFrame, text="to")
        self.to.grid(row=3, column=2, sticky="w")
        self.e2 = Entry(self.upperRangeFrame, width=8)
        self.e2.grid(row=3, column=3, sticky="w")

    def render(self):
        pass
    
root = Tk()
tool = ToolsWindow(root)
tool.setupToolBarButtons()
root.mainloop()

