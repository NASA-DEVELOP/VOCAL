from Tkinter import Toplevel, Entry, Button, Listbox, BOTH, LEFT, Frame, \
    RIGHT, TOP, Text, Label, RAISED, Menubutton, IntVar, Menu, END, Scrollbar, \
    VERTICAL, CENTER
    
from tools import center
import Constants

class dbDialog(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        self.title("Import from existing database")
        self.geometry('%dx%d+%d+%d' % (400, 600, 0, 0))
        center(self)
        
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.createTopFrame()
        self.createBottomFrame()
        
    def createTopFrame(self):
        # create top frame, do not expand out
        self.top_frame = Frame(self.container)
        self.top_frame.pack(side="top", fill="x", expand=False)
        
        # search label and entry
        self.label = Label(self.top_frame, text="Search ")
        self.label.grid(row=0, column=0, padx=5, pady=10)
        self.e = Entry(self.top_frame)
        self.e.grid(row=0, column=1, padx=5, pady=10)
        
        self.orderSelectionButton = Menubutton(self.top_frame, text="Order by", 
                                               relief=RAISED, width=10)
        self.orderSelectionButton.grid(row=0, column=2, padx=5, pady=10)
        self.orderSelectionButton.menu = Menu(self.orderSelectionButton, tearoff=0)
        self.orderSelectionButton["menu"] = self.orderSelectionButton.menu
        self.selection = IntVar()
        
        labels = [("File name",Constants.FILE_NAME), ("Color",Constants.COLOR), 
                  ("Attributes",Constants.ATTRIBUTES), ("Custom",Constants.CUSTOM)]
        
        for tx in labels:
            self.orderSelectionButton.menu.add_radiobutton(label=tx[0],
                                                           variable=self.selection,
                                                           value=tx[1],
                                                           command=self.order)
            
        self.filterButton = Button(self.top_frame, text="Filter", command=self.filterDialog,
                                   width=10)
        self.filterButton.grid(row=0, column=3, padx=5, pady=10)
        
    def createBottomFrame(self):
        self.bottom_frame = Frame(self.container)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)
        self.separator = Frame(self.bottom_frame, relief="ridge", height=2, bg="gray")
        self.separator.pack(side="top", fill="x", expand=False)
        self.bottomButtonFrame = Frame(self.bottom_frame)
        self.bottomButtonFrame.pack(side="bottom", fill="x", expand=False)
        
        self.listbox = Listbox(self.bottom_frame)
        self.listbox.pack(fill=BOTH, expand=True)
        
        self.scrollbar = Scrollbar(self.listbox, orient=VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill="y")
        
        for i in range(1, 10000):
            self.listbox.insert(END, str(i))
            
        self.button = Button(self.bottomButtonFrame, text="Import", width=30)
        self.button.pack(side="bottom", pady=10)
        
    def order(self):
        pass
    
    def filterDialog(self):
        pass
    
    def free(self):
        self.destroy()
        
