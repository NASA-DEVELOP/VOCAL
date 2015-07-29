###################################
#    Created on Jul 29, 2015
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

class Query(Observer):
    """
    Observer object that holds a *ranges* dictionary which can be used
    to query the database once updated. Notifies it's parent upon ranges
    being changed
    """
    def __init__(self):
        Observer.__init__(self)
        self._ranges = {}

    @property
    def ranges(self):
        return self._ranges

    @ranges.setter
    def ranges(self, n_ranges):
        self._ranges = n_ranges
        self.notify()

class AdvancedSearchDialog(Toplevel):
    """
    A dialog for advanced searching, notifying `ImportDialog` when search parameters have
    been chosen and entered. Uses the observer design pattern to notify ``ImportDialog``
    when the ranges have been changed from an invalid state to valid.

    :param parent: The class to attach the observer to
    :param root: The base widget for ``Toplevel``
    """

    def __init__(self, parent, root):
        Toplevel.__init__(self, root)

        self.title = 'Advanced search'
        self.shared_data = Query()
        self.shared_data.attach(parent)

        center(self, (constants.IMADVWIDTH, constants.IMADVHEIGHT))

        window_frame = Frame(self)
        window_frame.pack(fill=BOTH, expand=True)
        top_window_frame = Frame(window_frame)
        top_window_frame.pack(side=TOP, fill=X, expand=False)
        Label(top_window_frame, text='Filter by: ').pack(side=LEFT, padx=15, pady=5)
        Label(top_window_frame, text='Leave Items blank you do not wish to search by',
              font=('Helvetica', 8)).pack(side=RIGHT, padx=15, pady=5)
        bottom_window_frame = Frame(window_frame)
        bottom_window_frame.pack(side=TOP, fill=BOTH, expand=False, padx=15)
        bottom_window_frame.config(highlightthickness=1)
        bottom_window_frame.config(highlightbackground='grey')
        Label(bottom_window_frame, text='Plot ').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='Date ').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='Time Range ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='Latitude Range ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='File ').grid(row=4, column=0, padx=5, pady=5, sticky='w')

        self.plots = StringVar()
        self.am_pm = StringVar()
        self.plot_entry = OptionMenu(bottom_window_frame, self.plots, 'backscattered', 'depolarized', 'vfm')
        self.plot_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w', columnspan=3)

        self.date_entry = Entry(bottom_window_frame, width=25)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w', columnspan=4)
        self.date_entry.insert(END, '0000-00-00')

        self.b_time_entry = Entry(bottom_window_frame, width=10)
        self.b_time_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.b_time_entry.insert(END, '00:00:00')
        Label(bottom_window_frame, text='to').grid(row=2, column=2, pady=5, sticky='w')
        self.e_time_entry = Entry(bottom_window_frame, width=10)
        self.e_time_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.e_time_entry.insert(END, '00:00:00')

        self.am_pm_menu = OptionMenu(bottom_window_frame, self.am_pm, 'am', 'pm')
        self.am_pm_menu.grid(row=2, column=4, pady=5, sticky='w')

        self.b_lat_entry = Entry(bottom_window_frame, width=10)
        self.b_lat_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.b_lat_entry.insert(END, '0.0')
        Label(bottom_window_frame, text='to').grid(row=32, column=2, pady=5, sticky='w')
        self.e_lat_entry = Entry(bottom_window_frame, width=10)
        self.e_lat_entry.grid(row=3, column=3, padx=5, pady=5, sticky='w')
        self.e_lat_entry.insert(END, '0.0')

        self.file_entry = Entry(bottom_window_frame, width=25)
        self.file_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w', columnspan=4)

        bottom_button_frame = Frame(window_frame)
        bottom_button_frame.pack(side=TOP, fill=BOTH, expand=False)

        Button(bottom_button_frame, text='Search', command=self.parse_ranges).\
            pack(side=LEFT, padx=15, pady=10)

    def parse_ranges(self):

        self.shared_data.ranges = {'plots': self.plots.get(),
                                   'am_pm': self.am_pm.get()}
