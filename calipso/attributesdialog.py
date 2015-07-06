######################################
# Created on Jun 15, 2015
#
# @author: Grant Mercer
#
######################################

from Tkconstants import TOP, X, BOTH, BOTTOM, END, EXTENDED
from Tkinter import Toplevel, Frame, StringVar, Label, Text, Button, Listbox
from log import logger

import constants


class AttributesDialog(Toplevel):
    """
    Dialog window for creating and assigning attributes to objects

    :param root: The parent frame
    :param polygon_drawer: The polygonDrawer being edited
    """
    
    def __init__(self, root, polygon_drawer):
        """
        Initialize root tkinter window and master GUI window
        """
        Toplevel.__init__(self, root, width=200, height=200)
        
        self.__poly = polygon_drawer
        if polygon_drawer is False:
            self.close()
            return
        self.title('Edit Attributes')
        
        # copies TAGS to avoid aliasing
        self.__availableAttributes = constants.TAGS[:]
        
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.top_frame = None
        self.bottom_frame = None
        self.note_text = None
        self.attributes_list = None
        self.selected_list = None
            
        logger.info('Creating top frame')
        self.create_top_frame()
        logger.info('Creating bottom frame')
        self.create_bottom_frame()
        
    def create_top_frame(self):
        """
        Initializes the top half of the window
        """
        self.top_frame = Frame(self.container)
        self.top_frame.pack(side=TOP, fill=X, expand=False)
        
        attributes_string = StringVar()
        attributes_string.set('Attributes:')
        attributes_label = Label(self.top_frame, textvariable=attributes_string)
        attributes_label.grid(row=0, column=0)
        
        selected_string = StringVar()
        selected_string.set('Selected:')
        selected_label = Label(self.top_frame, textvariable=selected_string)
        selected_label.grid(row=0, column=3)
        
        self.attributes_list = Listbox(self.top_frame, width=30, height=30, selectmode=EXTENDED)
        self.attributes_list.grid(row=1, column=0)
        
        self.selected_list = Listbox(self.top_frame, width=30, height=30, selectmode=EXTENDED)
        self.selected_list.grid(row=1, column=3)
        
        logger.info('Loading attributes')
        for tag in self.__availableAttributes:
            if self.__poly.isInAttributes(tag):
                self.selected_list.insert(END, tag)
            else:
                self.attributes_list.insert(END, tag)
        
        remove_button = Button(self.top_frame, width=3, height=2, text='<--',
                               command=self.remove_attribute)
        remove_button.grid(row=1, column=1)
        
        move_button = Button(self.top_frame, width=3, height=2, text='-->',
                             command=self.move_attribute)
        move_button.grid(row=1, column=2)
        
    def create_bottom_frame(self):
        """
        Initializes the bottom half of the window
        """
        self.bottom_frame = Frame(self.container)
        self.bottom_frame.pack(side=BOTTOM, fill=X, expand=False)
        
        note_string = StringVar()
        note_string.set('Notes:')
        note_label = Label(self.bottom_frame, textvariable=note_string)
        note_label.grid(row=0, column=1)
        
        self.note_text = Text(self.bottom_frame, width=55, height=10)
        self.note_text.grid(row=1, column=1)
        self.note_text.insert(END, self.__poly.getNotes())
        
        button_frame = Frame(self.container)
        button_frame.pack(side=BOTTOM, fill=X, expand=False)
        
        accept_button = Button(button_frame, text='Save', command=self.save)
        accept_button.grid(row=0, column=0)
        
        cancel_button = Button(button_frame, text='Clear Note', command=self.clear)
        cancel_button.grid(row=0, column=1)
        
#         closeButton = Button(buttonFrame, text='Close', command=self.close)
#         closeButton.grid(row=3, column=2)
        
    def move_attribute(self):
        """
        Saves the attributes that the user has selected
        """
        logger.info('Setting attributes')
        selection = self.attributes_list.curselection()
        if len(selection) == 0:
            return
        for item in selection:
            string = self.attributes_list.get(item)
            self.__poly.addAttribute(string)
            self.selected_list.insert(END, string)
        for item in reversed(selection):
            self.attributes_list.delete(item)
    
    def remove_attribute(self):
        """
        Deletes the attributes that the user has selected
        """
        logger.info('Deleting attributes')
        selection = self.selected_list.curselection()
        if len(selection) == 0:
            return
        for item in selection:
            string = self.selected_list.get(item)
            self.__poly.remove_attribute()
            self.attributes_list.insert(END, string)
        for item in reversed(selection):
            self.selected_list.delete(item)
    
    def save(self):
        """
        Saves the note
        """
        logger.info('Saving note')
        note = self.note_text.get('1.0', 'end-1c')
        self.__poly.setNotes(note)
        self.close()
    
    def clear(self):
        """
        Deletes the note
        """
        logger.info('Deleting note')
        self.note_text.delete(1.0, END)
        self.__poly.setNotes('')
    
    def close(self):
        """
        Closes window
        """
        logger.info('Closing window')
        self.destroy()
