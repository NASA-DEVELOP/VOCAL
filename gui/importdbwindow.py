'''
Created on Jun 15, 2015

@author: Grant Mercer

'''
from Tkinter import Toplevel, Entry, Button, Listbox, BOTH, Frame, \
    RIGHT, Label, RAISED, Menubutton, IntVar, Menu, END, Scrollbar, \
    VERTICAL
    
from tools import center
import Constants
from gui.db import db, dbPolygon
#import db

class dbDialog(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        self.title("Import from existing database")
        center(self, (400,600))
        
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.createTopFrame()
        self.createBottomFrame()
        
    def createTopFrame(self):
        # create top frame, do not expand out
        self.topFrame = Frame(self.container)
        self.topFrame.pack(side="top", fill="x", expand=False)
        
        # search label and entry
        self.label = Label(self.topFrame, text="Search ")
        self.label.grid(row=0, column=0, padx=5, pady=10)
        self.e = Entry(self.topFrame)
        self.e.grid(row=0, column=1, padx=5, pady=10)
        
        self.orderSelectionButton = Menubutton(self.topFrame, text="Order by", 
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
            
        self.filterButton = Button(self.topFrame, text="Filter", command=self.filterDialog,
                                   width=10)
        self.filterButton.grid(row=0, column=3, padx=5, pady=10)
        
    def createBottomFrame(self):
        self.bottomFrame = Frame(self.container)
        self.bottomFrame.pack(side="bottom", fill="both", expand=True)
        self.separator = Frame(self.bottomFrame, relief="ridge", height=2, bg="gray")
        self.separator.pack(side="top", fill="x", expand=False)
        self.bottomButtonFrame = Frame(self.bottomFrame)
        self.bottomButtonFrame.pack(side="bottom", fill="x", expand=False)
        
        self.listbox = Listbox(self.bottomFrame)
        self.listbox.pack(fill=BOTH, expand=True)
        
        self.scrollbar = Scrollbar(self.listbox, orient=VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill="y")
        
        session = db.getSession()
        for obj in session.query(dbPolygon).all():
            self.listbox.insert(END, obj)
        session.close()
            
        self.button = Button(self.bottomButtonFrame, text="Import", width=30,
                             command=self.importSelection)
        self.button.pack(side="bottom", pady=10)
        
    def order(self):
        pass
    
    def importSelection(self):
        pass
    
    def filterDialog(self):
        pass
    
    def free(self):
        self.destroy()
        
