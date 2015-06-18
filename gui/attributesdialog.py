'''
Created on Jun 15, 2015

@author: Grant Mercer

'''

from Tkconstants import TOP, X, BOTH, DISABLED, BOTTOM, END, SEL_FIRST, SEL_LAST, \
    NORMAL
from Tkinter import Toplevel, Frame, StringVar, Label, Text, Button


class attributesDialog(Toplevel):
    '''
    Dialog window for creating and assigning attributes to objects
    '''
    def __init__(self, root, master, event):
        '''
        Initialize root tkinter window and master GUI window
        '''
        Toplevel.__init__(self, root, width=200, height=200)
        self.__master = master
        self.__event = event
        self.__selectedAttributes = []
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
        
        self.attributeText = Text(self.topFrame, width=30, height=30)
        self.attributeText.grid(row=1, column=0)
        self.attributeText.insert(END, "Cloud\n")
        self.attributeText.insert(END, "Aerosol\n")
        self.attributeText.config(state=DISABLED)
        
        removeButton = Button(self.topFrame, width=3, height=2, text="<--", command=self.removeAttribute)
        removeButton.grid(row=1, column=1)
        
        moveButton = Button(self.topFrame, width=3, height=2, text="-->", command=self.moveAttribute)
        moveButton.grid(row=1, column=2)
        
        self.selectedText = Text(self.topFrame, width=30, height=30)
        self.selectedText.grid(row=1, column=3)
        self.selectedText.config(state=DISABLED)
        
    def createBottomFrame(self):
        self.bottomFrame = Frame(self.container)                       
        self.bottomFrame.pack(side=BOTTOM, fill=X, expand=False)
        
        noteString = StringVar()
        noteString.set("Notes:")
        noteLabel = Label(self.bottomFrame, textvariable=noteString)
        noteLabel.grid(row=0, column=0)
        
        self.noteText = Text(self.bottomFrame, width=10, height=10)
        self.noteText.grid(row=1, column=0)
        
        acceptButton = Button(self.bottomFrame, text="Accept", command=self.accept)
        acceptButton.grid(row=2, column=0)
        
        cancelButton = Button(self.bottomFrame, text="Cancel", command=self.cancel)
        cancelButton.grid(row=2, column=1)
        
        closeButton = Button(self.bottomFrame, text="Close", command=self.close)
        closeButton.grid(row=2, column=2)
        
    def moveAttribute(self):
        print "Moving tag"
        selection = self.attributeText.get(SEL_FIRST, SEL_LAST)
        self.__selectedAttributes.append(selection)
        self.selectedText.config(state=NORMAL)
        self.selectedText.insert(END, selection + "\n")
        self.selectedText.config(state=DISABLED)
        self.attributeText.config(state=NORMAL)
#         self.attributeText.delete(1.0, float(len(selection)))
        self.attributeText.delete(1.0, 2.0)
        self.attributeText.config(state=DISABLED)
    
    def removeAttribute(self):
        pass
    
    def accept(self):
        pass
    
    def cancel(self):
        pass
    
    def close(self):
        self.destroy()