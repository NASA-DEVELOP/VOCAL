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
    Label, BOTTOM, TOP, X, RIDGE, Checkbutton, IntVar, OptionMenu, StringVar

import constants
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
        self.transient(root)
        self.shared_data = ExtractionList()
        self.shared_data.attach(parent)
        self.wm_iconbitmap(constants.ICO)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = w / 2 - 400
        y = h / 2

        Label(self, text='Columns:').pack(side=TOP, anchor='w')
        self.geometry('+%d+%d' % (x, y))
        column_map = dict()
        for title in parent.column_titles:
            column_map[title] = IntVar()
            Checkbutton(self, text=title, variable=column_map[title]).\
                pack(side=TOP, anchor='w')

