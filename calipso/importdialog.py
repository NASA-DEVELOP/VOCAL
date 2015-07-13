###################################
#    Created on Jun 15, 2015
#
#    @author: Grant Mercer
#
###################################
import collections
import tkMessageBox
import constants

from Tkinter import Toplevel, Entry, Button, BOTH, Frame, \
    Label, BOTTOM, TOP, X, RIDGE
from sqlalchemy import or_
from db import db, DatabasePolygon
from tools.tools import center, get_shape_ranges
from tools.treelistbox import TreeListBox
from log import logger


class ImportDialog(Toplevel):
    """
    Dialog window which prompts user for a selection of objects to import as well as
    showing a customizable list for displaying the data

    :param: root: root Tk widget, often Tk()
    :param: master: the main window, for access of polygonList
    """

    def __init__(self, root, master):
        logger.info('Instantiating ImportDialog')
        Toplevel.__init__(self, root)

        self.protocol('WM_DELETE_WINDOW')
        self.session = db.get_session()
        self.__internal_list = list()
        self.__stack = collections.deque(maxlen=15)
        self.__search_string = ''
        self.__master = master
        self.title('Import from existing database')
        self.tree = None
        self.e = None
        self.top_frame = None
        self.bottom_frame = None
        self.bottom_button_frame = None
        self.separator = None

        center(self, (constants.IMPORTWIDTH, constants.IMPORTHEIGH))

        self.container = Frame(self)  # create center frame,
        self.container.pack(side=TOP, fill=BOTH, expand=True)  # place

        self.create_top_frame()  # create the top frame and pack buttons / etc. on it
        self.create_bottom_frame()  # create the bottom frame and pack

    def create_top_frame(self):
        """
        Initialize the upper frame of the window in charge of buttons
        """
        logger.info('Creating top frame')
        self.top_frame = Frame(self.container)  # create top frame
        self.top_frame.pack(side=TOP, fill=X, expand=False)

        label = Label(self.top_frame, text='Search ')  # search label
        self.e = Entry(self.top_frame)  # input box for searching specific attributes
        self.e.bind('<KeyRelease>', self.refine_search)
        label.grid(row=0, column=0, padx=5, pady=10)
        self.e.grid(row=0, column=1, padx=5, pady=10)

        spacer = Label(self.top_frame, width=20)  # create space between frame outline
        spacer.grid(row=0, column=2)
        self.top_frame.columnconfigure(2, weight=1)

        # custom command for filtering objects by properties
        delete_button = Button(self.top_frame, text='Delete', command=self.delete_from_db,
                               width=10)
        delete_button.grid(row=0, column=3, padx=15)

    def refine_search(self, event):
        """
        Function to dynamically narrow the results of a search while the
        user types into the search bar. Checks if the character is
        alpha numeric , and if so queries the database for the combined
        string. A backend stack keeps track of past searches, when the
        user enters the backspace code a previous instance is popped
        and reloaded.
        :param event: search box events
        """
        # If character is a letter or number, add to search_string
        if event.char.isalnum():
            self.__search_string += event.char
        # If the entry box is NOT empty
        if self.e.get() != '':
            # But If a backspace is entered
            if event.char == '':
                # Remove one letter from search string and pop stack
                self.__search_string = self.__search_string[:-1]
                if self.__stack:
                    self.tree.info = self.__stack.pop()
                    self.tree.update()
            # Else if the character is alphanumeric
            elif event.char.isalnum():
                # Temporary variable to create new list
                lst = list()
                # For all objects in the database
                for obj in self.session.query(DatabasePolygon).filter(
                        or_(  # query the database for if search_string is contained in
                              DatabasePolygon.tag.contains(self.__search_string),
                              DatabasePolygon.attributes.contains(self.__search_string),
                              DatabasePolygon.notes.contains(self.__search_string))):
                    time_range, altitude_range = get_shape_ranges(obj.time_, obj.coordinates)
                    lst.append(  # append any objects that were returned by the query
                                 (obj.tag, obj.plot, time_range, altitude_range, obj.attributes[1:-1],
                                  obj.notes, obj.hdf))
                # Push new query onto the stack and set display to list
                self.__stack.append(self.tree.info)
                self.tree.info = lst
                self.tree.update()
        else:
            self.__search_string = ''
            self.__display_all()
        logger.info('Displaying refined search')

    def create_bottom_frame(self):
        """
        Create and display database in listbox, also add lower button frame for import
        button
        """
        logger.info('Creating bottom frame')
        self.bottom_frame = Frame(self.container)  # create bottom frame
        self.bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.separator = Frame(self.bottom_frame, relief=RIDGE, height=2,
                               bg='gray')  # tiny separator splitting the top and bottom frame
        self.separator.pack(side=TOP, fill=X, expand=False)
        self.bottom_button_frame = Frame(self.bottom_frame)  # bottom frame for import button
        self.bottom_button_frame.pack(side=BOTTOM, fill=X, expand=False)

        self.tree = TreeListBox(self.bottom_frame,
                                ['name', 'plot', 'time range', 'altitude range',
                                 'attributes', 'notes', 'file'])

        for obj in self.session.query(DatabasePolygon).all():
            self.__internal_list.append(obj)  # insert JSON obj representation into internal list

        self.__display_all()

        button = Button(self.bottom_button_frame, text='Import', width=30,
                        command=self.import_selection)
        button.pack(side=BOTTOM, pady=10)

    def import_selection(self):
        """
        Import selected objects from internal_list into program
        """
        items = self.tree.tree.selection()
        logger.info('Importing selection')
        # For all selected items in window
        for tag in items:
            # Find those items in internal list and import them
            logger.info('Encoding selection to JSON')
            tag = self.tree.tree.item(tag, option='values')
            names = [x.tag for x in self.__internal_list]
            logger.info('Forwarding JSON to be read')
            self.__master.get_shapemanager().read_plot(
                read_from_str=str(self.__internal_list[names.index(tag[0])]))
        logger.info('Done')
        self.free()

    def delete_from_db(self):
        """
        Delete selected objects from database
        """
        items = self.tree.tree.selection()
        if tkMessageBox.askyesno('Delete?', 'Really delete these items?', parent=self):
            for tag in items:
                tag = self.tree.tree.item(tag, option='values')
                idx = self.__internal_list[[x.tag for x in self.__internal_list].index(tag[0])].id
                logger.info('Notifying db of deletion for \'%s\' from selection' % tag[0])
                db.delete_item(idx)
            self.__display_all()
        logger.info('Done')

    def __display_all(self):
        """
        Helper function to simply display all objects in the database
        """
        logger.info('Displaying entries')
        lst = list()
        # Push previous display to stack
        if self.tree.info:
            self.__stack.append(self.tree.info)
        for obj in self.session.query(DatabasePolygon).all():
            time_range, altitude_range = get_shape_ranges(obj.time_, obj.coordinates)
            lst.append(  # user see's this list
                         (obj.tag, obj.plot, time_range, altitude_range, obj.attributes[1:-1], obj.notes, obj.hdf))

        self.tree.info = lst
        self.tree.update()

    def free(self):
        """
        Free window
        """
        logger.info('Closing window')
        self.session.commit()
        self.session.close()
        self.destroy()
