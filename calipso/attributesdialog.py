######################################
# Created on Jun 15, 2015
#
# @author: Grant Mercer
#
######################################

from Tkconstants import TOP, X, BOTH, BOTTOM, END, EXTENDED
from Tkinter import Toplevel, Frame, StringVar, Label, Text, Button, Listbox
import logging

import constants


class AttributesDialog(Toplevel):
    '''
    Dialog window for creating and assigning attributes to objects
    '''
    
    def __init__(self, root, polygonDrawer):
        '''
        Initialize root tkinter window and master GUI window
        :param root: the parent frame
        :param polygonDrawer: the polygonDrawer being edited
        '''
        logging.info("AttributesDialog: Instantiating AttributesDialog")
        Toplevel.__init__(self, root, width=200, height=200)
        
        self.__poly = polygonDrawer
        if polygonDrawer is False:
            self.close()
            return
        self.title("Edit Attributes")
        
        # copies TAGS to avoid aliasing
        self.__availableAttributes = constants.TAGS[:]
        
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True) 
            
        self.createTopFrame()
        self.createBottomFrame()
        
    def createTopFrame(self):
        '''
        Initializes the top half of the window
        '''
        logging.info("AttributesDialog: Creating top frame")
        self.topFrame = Frame(self.container)                       
        self.topFrame.pack(side=TOP, fill=X, expand=False)
        
        attributeString = StringVar()
        attributeString.set("Attributes:")
        attributeLabel = Label(self.topFrame, textvariable=attributeString)
        attributeLabel.grid(row=0, column=0)
        
        selectedString = StringVar()
        selectedString.set("Selected:")
        selectedLabel = Label(self.topFrame, textvariable=selectedString)
        selectedLabel.grid(row=0, column=3)
        
        self.attributeList = Listbox(self.topFrame, width=30, height=30, selectmode=EXTENDED)
        self.attributeList.grid(row=1, column=0)
        
        self.selectedList = Listbox(self.topFrame, width=30, height=30, selectmode=EXTENDED)
        self.selectedList.grid(row=1, column=3)
        
        for tag in self.__availableAttributes:
            if self.__poly.isInAttributes(tag):
                self.selectedList.insert(END, tag)
            else:
                self.attributeList.insert(END, tag)
        
        removeButton = Button(self.topFrame, width=3, height=2, text="<--", command=self.removeAttribute)
        removeButton.grid(row=1, column=1)
        
        moveButton = Button(self.topFrame, width=3, height=2, text="-->", command=self.moveAttribute)
        moveButton.grid(row=1, column=2)
        
    def createBottomFrame(self):
        '''
        Initializes the bottom half of the window
        '''
        logging.info("AttributesDialog: Creating bottom frame")
        self.bottomFrame = Frame(self.container)                       
        self.bottomFrame.pack(side=BOTTOM, fill=X, expand=False)
        
        noteString = StringVar()
        noteString.set("Notes:")
        noteLabel = Label(self.bottomFrame, textvariable=noteString)
        noteLabel.grid(row=0, column=1)
        
        self.noteText = Text(self.bottomFrame, width=55, height=10)
        self.noteText.grid(row=1, column=1)
        self.noteText.insert(END, self.__poly.getNotes())
        
        buttonFrame = Frame(self.container)
        buttonFrame.pack(side=BOTTOM, fill=X, expand=False)
        
        acceptButton = Button(buttonFrame, text="Save", command=self.save)
        acceptButton.grid(row=0, column=0)
        
        cancelButton = Button(buttonFrame, text="Clear Note", command=self.clear)
        cancelButton.grid(row=0, column=1)
        
#         closeButton = Button(buttonFrame, text="Close", command=self.close)
#         closeButton.grid(row=3, column=2)
        
    def moveAttribute(self):
        '''
        Saves the attributes that the user has selected
        '''
        logging.info("AttributesDialog: Setting attributes")
        selection = self.attributeList.curselection()
        if len(selection) == 0:
            return
        for item in selection:
            string = self.attributeList.get(item)
            self.__poly.addAttribute(string)
            self.selectedList.insert(END, string)
        for item in reversed(selection):
            self.attributeList.delete(item)
    
    def removeAttribute(self):
        '''
        Deletes the attributes that the user has selected
        '''
        logging.info("AttributesDialog: Deleting attributes")
        selection = self.selectedList.curselection()
        if len(selection) == 0:
            return
        for item in selection:
            string = self.selectedList.get(item)
            self.__poly.removeAttribute(string)
            self.attributeList.insert(END, string)
        for item in reversed(selection):
            self.selectedList.delete(item)
    
    def save(self):
        '''
        Saves the note
        '''
        logging.info("AttributesDialog: Saving note")
        note = self.noteText.get('1.0', 'end-1c')
        self.__poly.setNotes(note)
        self.close()
    
    def clear(self):
        '''
        Deletes the note
        '''
        logging.info("AttributesDialog: Deleting note")
        self.noteText.delete(1.0, END)
        self.__poly.setNotes("")
    
    def close(self):
        logging.info("AttributesDialog: Closing window")
        self.destroy()
