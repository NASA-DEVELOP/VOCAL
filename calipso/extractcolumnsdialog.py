###################################
#    Created on Aug 4, 2015
#
#    @author: Grant Mercer
#
###################################

from Tkconstants import LEFT, END, RIGHT
import collections
import tkMessageBox
from Tkinter import Toplevel, Entry, Button, BOTH, Frame, \
    Label, BOTTOM, TOP, X, RIDGE, Checkbutton, IntVar, OptionMenu, StringVar, Radiobutton

from constants import TXT, CSV, ICO
from sqlalchemy import or_
from db import db, DatabasePolygon
from tools.tools import center, get_shape_ranges, Observer
from tools.treelistbox import TreeListBox
from tools.tooltip import create_tool_tip
from log.log import logger
import re

class ExtractionList(Observer):
    """
    Observer object that holds a dictionary of key values that is passed
    into ImportDialog upon notifying a save action. The keys are used to
    extract the data.
    """
    def __init__(self):
        Observer.__init__(self)
        self._data = {}

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, n_data):
        self._data = n_data
        self.notify()

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.receive_extract_columns(self)


class ExtractColumnsDialog(Toplevel):
    """
    A dialog window for extracting certain columns to a user specified file format.
    The user can select which columns they would like to extract and generate either
    a ``.txt`` or ``.csv`` from the selected columns. Uses the Observer pattern to
    notify `ImportDialog` once a selection is made
    """

    def __init__(self, parent, root):
        Toplevel.__init__(self, root)

        self.title = 'Extract Columns'
        self.protocol('WM_DELETE_WINDOW', self.free)
        self.transient(root)
        self.wm_iconbitmap(ICO)

        self.shared_data = ExtractionList()
        self.shared_data.attach(parent)

        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = w / 2 - 400
        y = h / 2
        self.geometry('+%d+%d' % (x, y))

        window_frame = Frame(self)
        window_frame.pack(fill=BOTH, expand=True)
        top_window_frame = Frame(window_frame)
        top_window_frame.pack(side=TOP, fill=X, expand=False)
        Label(top_window_frame, text='Columns: ').pack(side=LEFT, padx=10, pady=5)
        bottom_window_frame = Frame(window_frame, highlightthickness=1,
                                    highlightbackground='grey')
        bottom_window_frame.pack(side=TOP, fill=BOTH, expand=False, padx=10)
        column_map = dict()
        i = j = 0
        for title in parent.column_titles:
            column_map[title] = IntVar()
            Checkbutton(bottom_window_frame, text=title, variable=column_map[title]).\
                grid(row=i, column=j, sticky='w')
            j += 1
            if j > 2:
                i += 1
                j = 0

        bottom_filetype_frame = Frame(window_frame, highlightthickness=1,
                                      highlightbackground='grey')
        bottom_filetype_frame.pack(side=TOP, expand=False, padx=10, pady=10, anchor='w')

        filetype_var = IntVar()
        Radiobutton(bottom_filetype_frame, text='*.txt', variable=filetype_var, value=TXT).\
            pack(side=LEFT)
        Radiobutton(bottom_filetype_frame, text='*.csv', variable=filetype_var, value=CSV).\
            pack(side=LEFT)

        bottom_button_frame = Frame(window_frame)
        bottom_button_frame.pack(side=TOP, fill=BOTH, expand=False, padx=10, pady=15)
        Button(bottom_button_frame, text='Extract to File', command=self.extract).pack(side=TOP)

    def extract(self):
        pass

    def free(self):
        """
        Free the window and notify ``ImportDialog`` that a new window can be created now
        """
        logger.info('Closing ExtractColumnsDialog')
        self.shared_data.data = {'free': True}
        self.destroy()
