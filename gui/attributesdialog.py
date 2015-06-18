'''
Created on Jun 15, 2015

@author: Grant Mercer

'''

from Tkconstants import TOP, X, BOTH, DISABLED
from Tkinter import Toplevel, Frame, StringVar, Label, Text, Button


class attributesDialog(Toplevel):
    '''
    Dialog window for creating and assigning attributes to objects
    '''
    def __init__(self, root, master):
        '''
        Initialize root tkinter window and master GUI window
        '''
        Toplevel.__init__(self, root, width=200, height=200)
        self.__master = master
        self.title("Edit Attributes")
        
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True) 
            
        self.createTopFrame()
        self.createBottomFrame()
        
    def createTopFrame(self):
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
        
        attributeText = Text(self.topFrame)
        attributeText.grid(row=1, column=0)
        attributeText.config(state=DISABLED)
        
        moveButton = Button(self.topFrame, width=3, height=2)
        moveButton.grid(row=1, column=1)
        
        removeButton = Button(self.topFrame, width=3, height=2)
        removeButton.grid(row=1, column=2)
        
        selectedText = Text(self.topFrame)
        selectedText.grid(row=1, column=3)
        selectedText.config(state=DISABLED)
        
    def createBottomFrame(self):
        self.bottomFrame = Frame(self.container)                       
        self.bottomFrame.pack(side=TOP, fill=X, expand=False)
        
        noteString = StringVar()
        noteString.set("Notes:")
        noteLabel = Label(self.bottomFrame, textvariable=noteString)
        noteLabel.grid(row=0, column=0)
        
        noteText = Text(self.bottomFrame)
        noteText.grid(row=1, column=0)
        
        acceptButton = Button(self.bottomFrame)
        acceptButton.grid(row=2, column=0)
        
        cancelButton = Button(self.bottomFrame)
        cancelButton.grid(row=2, column=1)
        
        closeButton = Button(self.bottomFrame)
        closeButton.grid(row=2, column=2)