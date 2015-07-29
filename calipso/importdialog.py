###################################
#    Created on Jun 15, 2015
#
#    @author: Grant Mercer
#
###################################
from Tkconstants import LEFT
import collections
import tkMessageBox
from Tkinter import Toplevel, Entry, Button, BOTH, Frame, \
    Label, BOTTOM, TOP, X, RIDGE, Checkbutton, IntVar, OptionMenu, StringVar

import constants
from sqlalchemy import or_
from db import db, DatabasePolygon
from tools.tools import center, get_shape_ranges, in_alt_range, \
    in_lat_range, in_time_range
from tools.treelistbox import TreeListBox
from tools.tooltip import create_tool_tip
from log.log import logger
from advancedsearchdialog import AdvancedSearchDialog


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
        self.transient(root)

        self.protocol('WM_DELETE_WINDOW', self.free)
        self.session = db.get_session()                 # import window holds a session
        self.__internal_list = list()                   # internal list of db objs
        self.__stack = collections.deque(maxlen=15)     # stack for searching
        self.__search_string = ''                       # search string
        self.__master = master                          # CALIPSO class
        self.__root = root
        self.title('Import from existing database')     # window title
        self.tree = None                                # tree viewing class
        self.e = None                                   # entry box for searching
        self.top_frame = None                           # top Tkinter frame
        self.bottom_frame = None                        # bottom Tkinter frame
        self.bottom_button_frame = None                 # bottom BUTTON Tkinter frame
        self.separator = None                           # separator line
        self.filter_file = IntVar()                     # int_var for filtering by file
        self.advance_dialog = False

        self.plot_type = StringVar()
        self.beg_time = None
        self.end_time = None
        self.beg_lat = None
        self.end_lat = None
        self.beg_alt = None
        self.end_alt = None
        self.file = None

        center(self, (constants.IMPORTWIDTH, constants.IMPORTHEIGH))

        self.container = Frame(self)    # create center frame,
        self.container.pack(side=TOP, fill=BOTH, expand=True)  # place

        self.create_top_frame()         # create the top frame and pack buttons / etc. on it
        self.create_bottom_frame()      # create the bottom frame and pack

    def create_top_frame(self):
        """
        Initialize the upper frame of the window in charge of buttons, in order:
        creates a top_frame, sets a 'Search' label and binds an entry box beside
        it, which calls ``refine_search`` upon a user releasing a key after pressing.
        Then binds the *delete* button to ``data_from_db``
        """
        logger.info('Creating top frame')
        self.top_frame = Frame(self.container)
        self.top_frame.pack(side=TOP, fill=X, expand=False)

        label = Label(self.top_frame, text='Search ')
        self.e = Entry(self.top_frame)
        create_tool_tip(self.e, 'Search in Name, Attributes, Notes')
        self.e.bind('<KeyRelease>', self.refine_search)
        label.grid(row=0, column=0, padx=5, pady=10)
        self.e.grid(row=0, column=1, padx=5, pady=10)

        check_button = Checkbutton(self.top_frame, text='Filter for this file',
                                   variable=self.filter_file,
                                   command=self.filter_by_current_file)
        check_button.grid(row=0, column=2, padx=5, pady=10)

        advanced_filter = Button(self.top_frame, text='Advanced',
                                 command=self.advanced_prompt)
        advanced_filter.grid(row=0, column=3, padx=5, pady=10)

        spacer = Label(self.top_frame, width=30)
        spacer.grid(row=0, column=4)
        self.top_frame.columnconfigure(4, weight=1)

        delete_button = Button(self.top_frame, text='Delete', command=self.delete_from_db,
                               width=10)
        delete_button.grid(row=0, column=5, padx=15)

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
                                ['name', 'plot', 'time range', 'latitude range',
                                 'altitude range', 'attributes', 'notes', 'last edited',
                                 'file'])

        for obj in self.session.query(DatabasePolygon).all():
            self.__internal_list.append(obj)  # insert JSON obj representation into internal list

        self.__display_all()

        button = Button(self.bottom_button_frame, text='Import', width=30,
                        command=self.import_selection)
        button.pack(side=BOTTOM, pady=10)

    def filter_by_current_file(self):
        """
        Command function for the check button located beside the entry box in Import Dialog.
        Lists all shapes given by only the current file when checked. If unchecked displays
        all entries.
        """
        if self.filter_file.get():
            fn = self.__master.get_file().rpartition('/')[2]
            lst = self.get_current_file_shapes()
            logger.info('Displaying %d shapes contained in %s' % (len(lst), fn))
            lst = [x for x in lst if x in self.tree.info]
            self.__stack.append(self.tree.info)
            self.tree.info = lst
            self.tree.update()
        else:
            self.tree.info = self.__stack.pop()
            self.tree.update()

    def get_current_file_shapes(self):
        """
        Return a list of all shapes contained in the current file, queries the
        database looking for all entries with the column *tag* that match the
        file returned by the rpartitioned ``Calipso.get_file()`` function

        :rtype: list
        """
        fn = self.__master.get_file().rpartition('/')[2]
        lst = list()
        for obj in self.session.query(DatabasePolygon).filter_by(
            hdf=fn
        ):
            time_range, altitude_range = get_shape_ranges(obj.coordinates)
            lst.append(
                (obj.tag, obj.plot, time_range, obj.lat, altitude_range, obj.attributes[1:-1],
                 obj.notes, obj.time_, obj.hdf))
        if not lst:
            logger.warning('Query returned None, no shapes found')
        return lst

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
        # append to search string
        if event.char:
            self.__search_string += event.char
        # if the entry box is NOT empty
        if self.e.get() != '':
            # but If a backspace is entered that means we want to pop the stack
            if event.char == '':
                # remove one letter from search string and pop stack
                self.__search_string = self.__search_string[:-1]
                if self.__stack:
                    self.tree.info = self.__stack.pop()
                    self.tree.update()
            # else if the character is alphanumeric
            elif event.char.isalnum():
                # temporary variable to create new list
                lst = list()
                # for all objects in the database
                for obj in self.session.query(DatabasePolygon).filter(
                        or_(  # query the database for if search_string is contained in
                              # self.__search_string.strip() to remove leading and ending spaces
                              DatabasePolygon.tag.contains(self.__search_string.strip()),
                              DatabasePolygon.attributes.contains(self.__search_string.strip()),
                              DatabasePolygon.notes.contains(self.__search_string.strip()))):
                    time_range, altitude_range = get_shape_ranges(obj.coordinates)
                    lst.append(  # append any objects that were returned by the query
                                 (obj.tag, obj.plot, time_range, obj.lat, altitude_range, obj.attributes[1:-1],
                                  obj.notes, obj.time_, obj.hdf))
                # push new query onto the stack and set display to list
                if self.filter_file.get():
                    sub_list = set(self.get_current_file_shapes())
                    lst = [x for x in lst if x in sub_list]
                self.__stack.append(self.tree.info)
                self.tree.info = lst
                self.tree.update()
        else:
            if self.filter_file.get():
                sub_list = set(self.get_current_file_shapes())
                self.__search_string = ''
                self.tree.info = sub_list
                self.tree.update()
            else:
                self.__search_string = ''
                self.__display_all()
        logger.info('Displaying refined search')

    def import_selection(self):
        """
        Import selected objects from internal_list into program
        """
        items = self.tree.tree.selection()
        logger.info('Parsing selection')
        # For all selected items in window
        skip = False
        for tag in items:
            # Find those items in internal list and import them
            tag = self.tree.tree.item(tag, option='values')
            fname = tag[-1]
            cfname = self.__master.get_file().rpartition('/')[2]
            if fname != cfname:
                skip = not tkMessageBox.\
                    askyesno('Unmatched files',
                             '%s is from a different file than currently'
                             % tag[0] +
                             ' loaded, proceed anyways? \ncurrent:%s \nloaded:%s'
                             % (tag[-1], cfname))
            if not skip:
                logger.info('Encoding \'%s\' to JSON' % tag[0])
                names = [x.tag for x in self.__internal_list]
                logger.info('Forwarding JSON to be read')
                self.__master.get_shapemanager().read_plot(
                    read_from_str=str(self.__internal_list[names.index(tag[0])]))
            else:
                logger.info('skipping loading for %s' % tag[0])
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

    def advanced_prompt(self):
        if not self.advance_dialog:
            AdvancedSearchDialog(self, self.__root)
            self.advance_dialog = True
        else:
            pass

    def __display_all(self):
        """
        Helper function to simply display all objects in the database
        """
        logger.info('Refreshing dialog view')
        lst = list()
        # Push previous display to stack
        if self.tree.info:
            self.__stack.append(self.tree.info)
        for obj in self.session.query(DatabasePolygon).all():
            time_range, altitude_range = get_shape_ranges(obj.coordinates)
            lst.append(  # user see's this list
                         (obj.tag, obj.plot, time_range, obj.lat, altitude_range, obj.attributes[1:-1],
                          obj.notes, obj.time_, obj.hdf))

        self.tree.info = lst
        self.tree.update()

    def receive(self, observer):
        """
        Receiving method called internally by an observer. When AdvancedSearchDialog is
        opened an observer is attached to this class, and upon the new ranges being updated
        this method is procd. The new ranges to query by are given by the dict received, so
        we can display the advanced search items.
        """

        rng = observer.ranges

        # TODO: Fix this implementation

        query_result = self.session.query(DatabasePolygon)

        if rng['plot']:
            query_result = query_result.filter(
                DatabasePolygon.plot.is_(rng['plot'])
            )

        if rng['file']:
            query_result = query_result.filter(
                DatabasePolygon.hdf.is_(rng['file'])
            )

        # This next part should NOT be considered a permanent solution

        lazy_list = list()

        for obj in query_result:
            time_range, altitude_range = get_shape_ranges(obj.coordinates)
            lazy_list.append(
                (obj.tag, obj.plot, time_range, obj.lat, altitude_range, obj.attributes[1:-1],
                 obj.notes, obj.time_, obj.hdf))

        lazy_list = [x for x in lazy_list if in_time_range(x[2]) and
                                             in_lat_range(x[3])]

    def free(self):
        """
        Commit the session, destroy the window and ensure the session is
        closed correctly
        """
        logger.info('Closing import window')
        self.session.commit()
        self.session.close()
        self.destroy()
