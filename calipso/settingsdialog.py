#############################
#    Created July 21, 2017
#
#    @author Collin Pampalone
#
#############################

import collections
import tkFileDialog
import tkMessageBox
from Tkinter import Toplevel, Entry, Button, BOTH, Frame, SUNKEN, \
    Label, LEFT, BOTTOM, TOP, X, RIDGE, Checkbutton, StringVar, BooleanVar, N, S, E, W, NE, SE, NW, SW, Grid, NORMAL, Radiobutton

from bokeh.colors import white

from Tkconstants import END

import constants
from datetime import datetime, time
from constants import CONF, CSV, TXT, DATEFORMAT, ICO
from sqlalchemy import or_, Time, cast
from db import db, DatabasePolygon
from tools.tools import center, get_shape_ranges, find_between, get_sec
from tools.treelistbox import TreeListBox
from tools.tooltip import create_tool_tip
from log.log import logger

class SettingsDialog(Toplevel):
    """
    Dialog Window that allows the user to manually change the settings in config.json
    """
    # This dialog should be a singleton, so the caller will ensure no other
    # windows are open by checking this variable
    singleton = False

    def __init__(self, root, master):
        SettingsDialog.singleton = True  # creation of a pseudo singleton

        logger.info('Instantiating SettingsDialog')
        Toplevel.__init__(self, root)
        self.transient(root)

        self.protocol('WM_DELETE_WINDOW', self.free)

        self.__root = root
        self.__master = master

        self.__var_dict = None
        self.__label_setting_dialogs = list()
        self.__buttons = list()
        self.__bool_buttons = list()
        self.__bool_button_frames = list()
        self.__checks = list()

        self.__top_frame = None
        self.__bottom_frame = None

        self.__container = Frame(self)
        self.__container.pack(side=TOP, fill=BOTH, expand=True)  # place

        self.get_variable_dict()
        self.create_top_frame()
        self.create_bottom_frame()

    def create_top_frame(self):
        self.__top_frame = Frame(self.__container)
        self.__top_frame.pack(side=TOP, fill=BOTH, expand=False)

        title_bar = []
        title_bar_text = ['Config Setting', 'Value', '','Lock']
        n = 0
        for text in title_bar_text:
            title_bar.append(Label(self.__top_frame, text=text))
            title_bar[n].grid(row=0, column=n, padx=5, pady=5, sticky=W)
            n += 1

        label_settings = []
        n = 0
        for key, value in self.__var_dict.iteritems():
            var_text = StringVar()
            var_text.set(str(value['value']))
            label_name = key + ':'
            check_val = BooleanVar()
            bool_value = BooleanVar()
            label_settings.append(Label(self.__top_frame, text=label_name))

            setting_type = self.__var_dict[key]['type']
            if setting_type == 'file':
                self.__label_setting_dialogs.append(Entry(self.__top_frame,
                                                          state='readonly', width=30, justify=LEFT,
                                                          textvariable=var_text,
                                                          readonlybackground=white, relief=SUNKEN))
                self.__buttons.append(Button(self.__top_frame, text='Change', width=10,
                                             command=lambda key=key, n=n:
                                             self.change_setting(key, self.__label_setting_dialogs[n])))
            elif setting_type == 'bool':
                self.__bool_buttons.append(Checkbutton(self.__top_frame, variable=bool_value, command=lambda key=key, bool_value=bool_value: self.change_bool_setting(key, bool_value), onvalue=True, offvalue=False))
                bool_value.set(value['value'])

            self.__checks.append(Checkbutton(self.__top_frame, variable=check_val,
                                             command=lambda key=key, check_val=check_val:
                                                 self.change_man_setting(key, check_val),
                                             onvalue=True, offvalue=False))
            check_val.set(value['man_setting'])
            label_settings[n].grid(row=(1 + n), column=0, padx=5, pady=5, sticky=W)

            if setting_type == 'file':
                self.__label_setting_dialogs[-1].grid(row=(1+n), column=1, padx=5, pady=5)
                self.__buttons[-1].grid(row=(1+n), column=2, pady=5, padx=5)
            elif setting_type == 'bool':
                self.__bool_buttons[-1].grid(row=(1+n), column=1, padx=5, pady=5)

            self.__checks[n].grid(row=(1+n), column=3, pady=5, padx=5)
            n += 1

        Grid.columnconfigure(self.__top_frame, 1, weight=1)

    def create_bottom_frame(self):
        self.__bottom_frame = Frame(self.__container)
        self.__bottom_frame.pack(side=BOTTOM, fill=X, expand=True)

        save_button = Button(self.__bottom_frame, text='Save Settings',
                             command=lambda: self.save())
        revert_button = Button(self.__bottom_frame, text='Revert Settings',
                               command=lambda: self.revert())
        save_button.grid(row=0, column=0, pady=5)
        revert_button.grid(row=0, column=1, pady=5)
        Grid.columnconfigure(self.__bottom_frame, 0, weight=1)
        Grid.columnconfigure(self.__bottom_frame, 1, weight=1)

    def change_man_setting(self, key, new_val):
        print(key)
        self.__var_dict[key]['man_setting'] = new_val.get()
        print(self.__var_dict)

    def change_bool_setting(self, key, new_value):
        print(new_value)
        print(key)
        self.__var_dict[key]['value'] = new_value.get()
        print(self.__var_dict)

    def change_setting(self, key, dialog_box):
        """ change this so it works with the self dict keys """
        setting_type = self.__var_dict[key]['type']
        if setting_type == 'file':
            directory = tkFileDialog.askdirectory()
            if directory != '':
                dialog_box.config(state=NORMAL)
                dialog_box.delete(0, END)
                dialog_box.insert(END, directory)
                self.__var_dict[key]['value'] = directory
        elif setting_type == 'bool':
            dialog_box.delete(0, END)
            dialog_box.insert(END, self.__var_dict[key]['value'])
        print(self.__var_dict)

    def get_variable_dict(self):
        var_dict = CONF.get_variable_dict()
        new_dict = dict()
        for key, variable in var_dict.iteritems():
            key = key.replace('_', ' ')
            key = key.title()
            new_dict[key] = {
                'value': variable.value(),
                'man_setting': variable.manual_setting(),
                'type': variable.get_type()
            }
        self.__var_dict = new_dict

    def free(self):
        """
        Commit the session, destroy the window and ensure the session is
        closed correctly
        """
        # Singleton no longer exists, so set it to false
        SettingsDialog.singleton = False
        logger.info('Closing SettingsDialog')
        self.destroy()

    def save(self):
        writing_dict = CONF.get_variable_dict()
        for key, variable in self.__var_dict.iteritems():
            key = key.replace(' ', '_')
            key = key.lower()
            writing_dict[key].force_change(variable['value'])
            writing_dict[key].change_manual(variable['man_setting'])
        logger.info('Settings saved')
        self.free()

    def revert(self):
        self.get_variable_dict()
        self.__top_frame.destroy()
        self.__label_setting_dialog = None
        self.__label_setting_dialogs = list()
        self.__buttons = list()
        self.__checks = list()
        self.__top_frame = Frame(self)  # create center frame,
        self.__top_frame.pack(side=TOP, fill=BOTH, expand=True)  # place
        self.create_top_frame()

