'''
Created on Jun 15, 2015

@author: Grant Mercer

'''

import collections
from Tkinter import Toplevel, Entry, Button, BOTH, Frame, \
    Label, BOTTOM, TOP, X, RIDGE
import tkMessageBox

from calipso import constants
from calipso.db import db, dbPolygon
from calipso.tools.treelistbox import TreeListBox
from calipso.tools.tools import center
from sqlalchemy import or_
#import TkTreectrl as treectrl
#import db

class dbDialog(Toplevel):
    '''
    Dialog window which prompts user for a selection of objects to import as well as
    showing a customizable list for displaying the data
    '''
    def __init__(self, root, master):
        '''
        :param: root: root tk widget, often Tk()
        :param: master: the main window, for access of polygonList
        '''
        Toplevel.__init__(self, root)
        self.protocol('WM_DELETE_WINDOW')
                
        self.session = db.getSession()
        self.__itList = list()
        self.__stack = collections.deque(maxlen=15)
        self.__searchString = ""
        self.__master = master        
        self.title("Import from existing database")
        center(self, (constants.IMPORTWIDTH,constants.IMPORTHEIGH)) # simple function to center window and set size
        
        self.container = Frame(self)                                # create center frame, for use of splitting window horizontally later
        self.container.pack(side=TOP, fill=BOTH, expand=True)       # place
        
        self.createTopFrame()                                       # create the top frame and pack buttons / etc. on it
        self.createBottomFrame()                                    # create the bottom frame and pack
        
    def createTopFrame(self):
        '''
        Initialize the upper frame of the window in charge of buttons
        '''
        self.topFrame = Frame(self.container)                       # create top frame
        self.topFrame.pack(side=TOP, fill=X, expand=False)
        
        self.label = Label(self.topFrame, text="Search ")           # search label 
        self.e = Entry(self.topFrame)                               # input box for searching specific attributes
        self.e.bind("<KeyRelease>", self.refineSearch)
        self.label.grid(row=0, column=0, padx=5, pady=10)
        self.e.grid(row=0, column=1, padx=5, pady=10)
            
        lblSpace1 = Label(self.topFrame, width=20)     # create space between frame outline
        lblSpace1.grid(row=0, column=2)
        self.topFrame.columnconfigure(2, weight=1)
            
        # custom command for filtering objects by properties
        self.deleteButton = Button(self.topFrame, text="Delete", command=self.deleteDb,
                                   width=10)
        self.deleteButton.grid(row=0, column=3, padx=15)
        
    def refineSearch(self, event):
        '''
        Function to dynamically narrow the results of a search while the
        user types into the search bar. Checks if the character is 
        alpha numeric , and if so queries the database for the combined
        string. A backend stack keeps track of past searches, when the
        user enters the backspace code a previous instance is popped
        and reloaded.
        :param event: search box events
        '''
        if event.char.isalnum(): self.__searchString += event.char                  # if character is a letter / number, add to the searchstring
        if self.e.get() != '':                                                      # if the entry box is NOT empty
            if event.char == '':                                                    # if a backspace code is entered
                self.__searchString = self.__searchString[:-1]                      # remove one letter from search string
                if self.__stack :                                                   # pop previous search and display to tree
                    self.tree.info = self.__stack.pop()
                    self.tree.update()
            elif event.char.isalnum():                                              # else if the character is alphanumeric
                lst = list()
                for obj in self.session.query(dbPolygon).filter(or_(                # query the database for if self.__searchstring is contained in 
                        dbPolygon.tag.contains(self.__searchString),                # fields listed
                        dbPolygon.attributes.contains(self.__searchString),
                        dbPolygon.notes.contains(self.__searchString))):
                    lst.append(                                                     # append any objects that were returned by the query
                        (obj.tag, obj.plot, obj.time_, obj.hdf, obj.attributes[1:-1], obj.notes)
                    )
                self.__stack.append(self.tree.info)                                 # push the new list onto our stack
                self.tree.info = lst                                                # set the new display list and update
                self.tree.update()
        else:
            self.__searchString = ""
            self.__displayAll()
        
    def createBottomFrame(self):
        '''
        Create and display database in listbox, also add lower button frame for import
        button
        '''
        self.bottomFrame = Frame(self.container)                                            # create bottom frame
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=True)          
        self.separator = Frame(self.bottomFrame, relief=RIDGE, height=2, bg="gray")         # tiny separator splitting the top and bottom frame
        self.separator.pack(side=TOP, fill=X, expand=False)
        self.bottomButtonFrame = Frame(self.bottomFrame)                                    # bottom frame for import button
        self.bottomButtonFrame.pack(side=BOTTOM, fill=X, expand=False)
        
        self.tree = TreeListBox(self.bottomFrame,
            ['name', 'plot', 'date', 'file', 'attributes', 'notes'])
        
        for obj in self.session.query(dbPolygon).all():
            self.__itList.append(obj)                                                       # insert JSON obj representation into internal list
        
        self.__displayAll()
           
        self.button = Button(self.bottomButtonFrame, text="Import", width=30,
                             command=self.importSelection)
        self.button.pack(side=BOTTOM, pady=10)
    
    def importSelection(self):
        '''
        Import selected objects from libox into program
        '''
        items = self.tree.tree.selection()
        for tag in items:
            tag = self.tree.tree.item(tag, option="values")
            names = [x.tag for x in self.__itList]
            self.__master.getPolygonList().readPlot(
                readFromString=str(self.__itList[names.index(tag[0])]))
        self.free()
            
    def deleteDb(self):
        '''
        Delete selected objects from database
        '''
        items = self.tree.tree.selection()
        if tkMessageBox.askyesno("Delete?", "Really delete these items?", parent=self):
            for tag in items:
                tag = self.tree.tree.item(tag, option="values")
                idx = self.__itList[[x.tag for x in self.__itList].index(tag[0])].id
                db.deleteItem(idx)
            self.__displayAll()
    
    def __displayAll(self):
        '''
        Helper function to simply display all objects in the database
        '''
        lst = list()
        self.__offset = 0
        if self.tree.info : self.__stack.append(self.tree.info)
        for obj in self.session.query(dbPolygon).all():
            lst.append(                                                          # user see's this list
                (obj.tag, obj.plot, obj.time_, obj.hdf, obj.attributes[1:-1], obj.notes)
            )
            
        self.tree.info = lst
        self.tree.update()
        
    def free(self):
        '''
        Free window
        '''
        self.session.commit()
        self.session.close()
        self.destroy()
        
