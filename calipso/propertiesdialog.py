###################################
#    Created on Aug 9, 2015
#
#    @author: Grant Mercer
#
###################################
from Tkconstants import FLAT, RIGHT, LEFT
import collections
import tkFileDialog
import tkMessageBox
from Tkinter import Toplevel, Entry, Button, BOTH, Frame, \
    Label, BOTTOM, TOP, X, RIDGE, Checkbutton, IntVar, StringVar, TclError

import constants
from constants import CSV, TXT
from sqlalchemy import or_
from db import db, DatabasePolygon
from tools.tools import center, get_shape_ranges
from tools.treelistbox import TreeListBox
from tools.tooltip import create_tool_tip
from log.log import logger
from advancedsearchdialog import AdvancedSearchDialog
from extractcolumnsdialog import ExtractColumnsDialog

class PropertyDialog(Toplevel):
    """
    Displays the porperties of the shape in a window
    """
    dialogs = []

    def __init__(self, root, shape):
        logger.info('Instantiating PropertyDialog')
        Toplevel.__init__(self)
        self.root = root
        self.protocol('WM_DELETE_WINDOW', self.free)
        self.wm_overrideredirect(1)
        self.\
            geometry('+%d+%d' %
                     (root.winfo_pointerx() - 60,
                      root.winfo_pointery()))
        try:
            self.tk.call('::Tk::unsupported::MacWindowStyle',
                                         'style', self._w,
                                         'help', 'noActivates')
        except TclError:
            pass
        window_frame = Frame(self)
        window_frame.pack(side=TOP, fill=BOTH, expand=True)
        exit_frame = Frame(window_frame, background='#ffffe0')
        exit_frame.pack(side=TOP, fill=X, expand=True)
        button = Button(exit_frame, text='x', width=3, command=self.free,
               background='#ffffe0', highlightthickness=0, relief=FLAT)
        button.pack(side=RIGHT)
        text_frame = Frame(window_frame)
        text_frame.pack(side=TOP, fill=BOTH, expand=True)
        label = Label(text_frame, text=str(shape), justify=LEFT,
                      background='#ffffe0',
                      font=('tahoma', '8', 'normal'))
        label.pack(ipadx=1)
        PropertyDialog.dialogs.append(self)
        self.attributes("-topmost", True)

    def free(self):
        self.destroy()
        for val, widget in enumerate(PropertyDialog.dialogs):
            if widget is self:
                PropertyDialog.dialogs.pop(val)
                break
        if PropertyDialog.dialogs:
            for widget in PropertyDialog.dialogs:
                widget.lift(aboveThis=self.root)

