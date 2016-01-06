###################################
#    Created on Jun 15, 2015
#
#    @author: Grant Mercer
#
###################################
import collections
import tkFileDialog
import tkMessageBox
from Tkinter import Toplevel, Entry, Button, BOTH, Frame, \
    Label, BOTTOM, TOP, X, RIDGE, Checkbutton, IntVar, StringVar

import constants
from constants import CSV, TXT
from sqlalchemy import or_
from db import db, DatabasePolygon
from tools.tools import center, get_shape_ranges, find_between, get_sec
from tools.treelistbox import TreeListBox
from tools.tooltip import create_tool_tip
from log.log import logger
from advancedsearchdialog import AdvancedSearchDialog
from extractcolumnsdialog import ExtractColumnsDialog


class ImportDialog(Toplevel):
    """
    Dialog window which prompts user for a selection of objects to import as well as
    showing a customizable list for displaying the data

    :param: root: root Tk widget, often Tk()
    :param: master: the main window, for access of polygonList
    """

    # This dialog should be a singleton, so the caller will ensure no other
    # windows are open by checking this variable
    singleton = False

    def __init__(self, root, master):
        ImportDialog.singleton = True                   # creation of a pseudo singleton

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
        self.extract_dialog = False
        self.column_titles = ['name', 'plot', 'time range', 'latitude range',
                              'altitude range', 'attributes', 'notes', 'last edited',
                              'file']

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

        reset = Button(self.top_frame, text='Reset',
                       command=self.reset)
        reset.grid(row=0, column=4, padx=5, pady=10)


        spacer = Label(self.top_frame, width=30)
        spacer.grid(row=0, column=5)
        self.top_frame.columnconfigure(5, weight=1)


        delete_button = Button(self.top_frame, text='Delete', command=self.delete_from_db,
                               width=10)
        delete_button.grid(row=0, column=6, padx=15)

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

        self.tree = TreeListBox(self.bottom_frame, self.column_titles)

        for obj in self.session.query(DatabasePolygon).all():
            self.__internal_list.append(obj)  # insert JSON obj representation into internal list

        self.__display_all()

        Label(self.bottom_button_frame, width=35).grid(row=0, column=0)

        Button(self.bottom_button_frame, text='Import', width=30,
               command=self.import_selection).grid(row=0, column=1, padx=10, pady=10)

        Button(self.bottom_button_frame, text='Extract Column Contents', width=25,
               command=self.extract_columns_dialog).grid(row=0, column=2, padx=10, pady=10)

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
            # Only return list of objects in the current view, otherwise we would
            # just append lst
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
        logger.info('Opening advanced search window')
        if(not AdvancedSearchDialog.singleton):
            AdvancedSearchDialog(self, self.__root)
        else:
            logger.warning('Found existing advanced search window, canceling')

    def extract_columns_dialog(self):
        if not self.extract_dialog:
            ExtractColumnsDialog(self, self.__root)
            self.extract_dialog = True
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

    def reset(self):
        """
        Reset the view of the tree within the import window, clears the stack as well
        """
        logger.info('Resetting tree view & stack')
        self.__display_all()
        self.__stack.clear()

    def receive_advanced_search(self, observer):
        """
        Receiving method called internally by an observer. When AdvancedSearchDialog is
        opened an observer is attached to this class, and upon the new ranges being updated
        this method is procd. The new ranges to query by are given by the dict received, so
        we can display the advanced search items. Below is a list of all items within the
        dictionary, with the format Key -> Format -> Type -> Desc

        date  -> '0000-00-00' -> y-m-d  -> The outer date of the time range
        btime -> '00-00-00'   -> hr-m-s -> Beginning time range (*btime* -> *etime*)
        etime -> '00-00-00'   -> hr-m-s -> Ending time range
        blat  -> '0.0'        -> float  -> Beginning latitude range (*blat* -> *elat*)
        elat  -> '0.0'        -> float  -> Ending latitude range
        balt  -> '0.0'        -> float  -> Beginning altitude range (*balt* -> *ealt*)
        ealt  -> '0.0'        -> float  -> Ending altitude range
        plot  -> PLOTS        -> string -> Type of plot ('backscattered' etc..)
        ampm  -> 'am'/'pm'    -> string -> Whether the time range is AM or PM
        file  -> '.....hdf'   -> string -> File name

        :param observer: An ``advancedsearchdialog.Query`` object
        """
        if 'free' in observer.ranges:
            self.advance_dialog = False
            return

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

        lazy_list = list()

        for obj in query_result:
            time_range, altitude_range = get_shape_ranges(obj.coordinates)

            # If we're parsing a date, we can't just filter as we must transform
            # coordinates into time_range first, so we need to manually check and
            # skip which is PROBABLY not the best solution.
            if rng['date'] and rng['date'] not in time_range:
                continue

            if rng['btime'] and get_sec(rng['btime']) > \
                get_sec(find_between(time_range, ", ", " ")):
                continue

            if rng['etime'] and get_sec(rng['etime']) < \
                get_sec(find_between(time_range, "- ", " ")):
                continue

            lazy_list.append(
                (obj.tag, obj.plot, time_range, obj.lat, altitude_range, obj.attributes[1:-1],
                 obj.notes, obj.time_, obj.hdf))

        self.tree.info = lazy_list
        self.tree.update()

    def receive_extract_columns(self, observer):
        """
        Receiving method called internally by an observer bound to an ``ExtractColumnsDialog``
        instance. Upon the creation of a ``ExtractColumnDialog`` instance an observer is attached
        to the `ImportDialog`. Once the user finalizes the extraction details this function will
        be called with a dictionary of value .

        :param observer: An ``extractcolumnsdialog.ExtractionList`` object
        """
        if 'free' in observer.data:
            self.extract_dialog = False
            return

        columns_to_extract = [x for x in observer.data if observer.data[x] == 1 and
                              x in self.column_titles]
        filetype = observer.data['filetype']
        dataset = [[self.tree.tree.set(child, x) for child in self.tree.tree.get_children('')]
                   for x in columns_to_extract]

        if len(columns_to_extract) == 0:
            logger.error('No columns selected for extraction')
            tkMessageBox.showerror('Extract Columns', 'No columns selected for extraction')
            return

        if filetype == TXT:
            f = tkFileDialog.\
                asksaveasfilename(defaultextension='.txt',
                                  filetypes=[('text files', '*.txt'), ('All files', '*')])
            if f == '':
                logger.info('canceling export column data as txt')
                return
            with open(f, 'w+') as outfile:
                outfile.write(' '.join(columns_to_extract) + '\n')
                for i in range(0, len(dataset[0])):
                    for j in range(0, len(dataset)):
                        outfile.write(str(dataset[j][i]) + ' ')
                    outfile.write('\n')
        if filetype == CSV:
            f = tkFileDialog.\
                asksaveasfilename(defaultextension='.csv',
                                  filetypes=[('csv files', '*.csv'), ('All files', '*')])
            if f == '':
                logger.info('canceling export column data as csv')
                return
            logger.info('Writing to .csv')
            dataset.insert(0, columns_to_extract)
            with open(f, 'w+') as outfile:
                for i in range(len(dataset[0])):
                    if i == len(dataset[0]) - 1:
                        outfile.write(str(dataset[0][i]))
                    else:
                        outfile.write(str(dataset[0][i]) + ',')
                outfile.write('\n')
                for i in range(len(dataset[1])):
                    for j in range(1, len(dataset)):
                        if j == len(dataset) - 1:
                            outfile.write(str(dataset[j][i]))
                        else:
                            outfile.write(str(dataset[j][i]) + ',')
                    outfile.write('\n')
                
    def free(self):
        """
        Commit the session, destroy the window and ensure the session is
        closed correctly
        """
        # Singleton no longer exists, so set it to false
        ImportDialog.singleton = False
        logger.info('Closing ImportDialog')
        self.session.commit()
        self.session.close()
        self.destroy()
