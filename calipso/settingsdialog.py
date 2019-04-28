#############################
#    Created July 21, 2017
#
#    @author Collin Pampalone
#
#############################

import tkMessageBox
import tkFileDialog
from Tkinter import Toplevel, Entry, Button, BOTH, Frame, SUNKEN, Label, LEFT, BOTTOM, TOP, X, \
    Checkbutton, StringVar, BooleanVar, W, Grid, NORMAL

# from bokeh.colors import white
from Tkconstants import END
from constants import CONF
from log.log import logger
from os.path import dirname


class SettingsDialog(Toplevel):
    """
    Dialog Window that allows the user to manually change the settings in config.json
    """
    # This dialog should be a singleton, so the caller will ensure no other
    # windows are open by checking this variable
    singleton = False

    def __init__(self, root, master):
        SettingsDialog.singleton = True  # Creation of a pseudo singleton

        # Set up the window as transient, i.e. it is a subset the main window
        logger.info('Instantiating SettingsDialog')
        Toplevel.__init__(self, root)
        self.transient(root)

        self.protocol('WM_DELETE_WINDOW', self.free)  # Custom exit protocol

        self.__root = root  # Declare the inputs, root is the Tk root, master is Calipso
        self.__master = master

        self.__var_dict = None              # A formatted copy of config.json to hold changes
        self.__settings_entries = list()    # The text boxes for files settings, holds Entry objects
        self.__browse_buttons = list()      # Holds the browse buttons
        self.__bool_buttons = list()        # Holds the boolean setting checkboxes
        self.__lock_setting_buttons = list()     # Holds the lock setting checkboxes

        self.__top_frame = None
        self.__bottom_frame = None

        self.__container = Frame(self)  # Main frame to hold top and bottom
        self.__container.pack(side=TOP, fill=BOTH, expand=True)  # Place the frame

        self.get_variable_dict()  # Grab config file settings
        self.create_top_frame()  # Make the top and bottom frames
        self.create_bottom_frame()

    def create_top_frame(self):
        """ The top frame holds all of the widgets for displaying and changing settings """
        self.__top_frame = Frame(self.__container)  # Create and place the frame
        self.__top_frame.pack(side=TOP, fill=BOTH, expand=False)

        # Create the title bar to explain the contents of each column
        title_bar = []
        title_bar_text = ['Config Setting', 'Value', '', 'Lock']
        n = 0
        for text in title_bar_text:
            # Iterate through the column titles, create labels, and place them on the grid
            title_bar.append(Label(self.__top_frame, text=text))
            title_bar[n].grid(row=0, column=n, padx=5, pady=5, sticky=W)
            n += 1

        # Create a row for each setting with the necessary widgets for changing it
        label_settings = []
        n = 0
        for key, value in self.__var_dict.iteritems():
            # By iterating through, we can change the number and types of settings in config.py and
            # we don't have to make any changes to the settings dialog as long as it is a bool or
            # file directory
            var_text = StringVar()  # Temporary holds a string of the current directory
            var_text.set(str(value['value']))
            label_name = key + ':'  # Temporarily holds the label of the setting
            lock_val = BooleanVar()  # Temporarily holds the value of lock_setting
            bool_value = BooleanVar()  # Temporarily holds the value of a bool setting

            # Create the setting label
            label_settings.append(Label(self.__top_frame, text=label_name))

            # Figure out if we are making a file-type or bool-type setting
            setting_type = self.__var_dict[key]['type']
            if setting_type == 'file':
                # Create a readonly entry to display the string of the directory path
                self.__settings_entries.append(Entry(self.__top_frame, state='readonly', width=30,
                                                     justify=LEFT, textvariable=var_text,
                                                     readonlybackground='white', relief=SUNKEN))
                # Create a browse button to change the path
                dialog_box = self.__settings_entries[-1]
                self.__browse_buttons.append(
                    Button(self.__top_frame, text='Change', width=10, command=lambda key=key, dialog_box=dialog_box:
                           self.change_dir_setting(key, dialog_box)))
            elif setting_type == 'bool':
                # Create a checkbutton to switch bool values
                self.__bool_buttons.append(
                    Checkbutton(self.__top_frame, variable=bool_value, onvalue=True, offvalue=False,
                                command=lambda key=key, bool_value=bool_value:
                                self.change_bool_setting(key, bool_value)))
                # Set the checkbox to show the current config value
                bool_value.set(value['value'])

            # Create checkbutton to switch the value between
            # locked (true, set to manual) or not (false, auto)
            self.__lock_setting_buttons.append(
                Checkbutton(self.__top_frame, variable=lock_val, onvalue=True, offvalue=False,
                            command=lambda key=key, check_val=lock_val:
                            self.change_lock_setting(key, check_val)))
            # Set the checkbox to show the current config value
            lock_val.set(value['lock_setting'])

            # Place all of the widgets on the grid
            label_settings[n].grid(row=(1 + n), column=0, padx=5, pady=5, sticky=W)
            # Make sure we only place the correct widget
            if setting_type == 'file':
                self.__settings_entries[-1].grid(row=(1 + n), column=1, padx=5, pady=5)
                self.__browse_buttons[-1].grid(row=(1 + n), column=2, pady=5, padx=5)
            elif setting_type == 'bool':
                self.__bool_buttons[-1].grid(row=(1 + n), column=1, padx=5, pady=5)
            self.__lock_setting_buttons[n].grid(row=(1 + n), column=3, padx=5, pady=5)
            n += 1

        # Give the entry boxes, bool checkboxes in column 1 the ability to move with the window
        Grid.columnconfigure(self.__top_frame, 1, weight=1)

    def create_bottom_frame(self):
        """ The bottom frame which holds the save and revert buttons """
        # TODO add a default button to reset config.json to defaults
        self.__bottom_frame = Frame(self.__container)
        self.__bottom_frame.pack(side=BOTTOM, fill=X, expand=True)

        # Create a save and close button to save config
        save_button = Button(self.__bottom_frame, text='Save Settings', command=lambda: self.save())
        # Create a revert button to scrap the changes and go back to the initial settings
        revert_button = Button(self.__bottom_frame, text='Revert Settings',
                               command=lambda: self.revert())
        # Place all of the buttons and ability to move
        save_button.grid(row=0, column=0, pady=5)
        revert_button.grid(row=0, column=1, pady=5)
        Grid.columnconfigure(self.__bottom_frame, 0, weight=1)
        Grid.columnconfigure(self.__bottom_frame, 1, weight=1)

    def change_lock_setting(self, key, new_val):
        """ Change the manual/auto lock setting """
        self.__var_dict[key]['lock_setting'] = new_val.get()
        logger.info(key + ' manual/auto lock changed to ' + str(new_val.get()))

    def change_bool_setting(self, key, new_val):
        """ Change a boolean config setting """
        self.__var_dict[key]['value'] = new_val.get()
        logger.info(key + ' bool setting changed to ' + str(new_val.get()))

    def change_dir_setting(self, key, dialog_box):
        """ Change a directory config setting """
        options = dict()
        if 'database' in key.lower():
            options['filetypes'] = [('CALIPSO Database', '*.db'), ('All files', '*')]
        elif 'hdf' in key.lower():
            options['filetypes'] = [('CALIPSO Data File', '*.hdf'), ('All files', '*')]
        options['initialdir'] = dirname(dialog_box.get())
        directory = tkFileDialog.askopenfilename(**options)
        if directory != '':     # if dir is not empty
            dialog_box.config(state=NORMAL)
            dialog_box.delete(0, END)
            dialog_box.insert(END, directory)
            self.__var_dict[key]['value'] = directory
        logger.info(key + ' file setting changed to ' + directory)

    def get_variable_dict(self):
        """ Load the dictionary of  variables from config.py through CONF in constants """
        # The dict must be copied this way so that we can make changes without referencing the
        # actual variables named in the CONF dictionary
        var_dict = CONF.get_variable_dict()
        new_dict = dict()
        for key, variable in var_dict.iteritems():  # Iterate through the dict to copy it
            key = key.replace('_', ' ')
            key = key.title()
            new_dict[key] = {
                'value': variable.value(),
                'lock_setting': variable.manual_setting(),
                'type': variable.get_type()
            }
        self.__var_dict = new_dict

    def free(self):
        """ Destroy the window and ensure the session is closed correctly """
        SettingsDialog.singleton = False    # Singleton no longer exists, so set it to false
        logger.info('Closing SettingsDialog')
        self.destroy()

    def save(self):
        """ Write all of the settings from the self.__var_dict to config.json and close"""
        writing_dict = CONF.get_variable_dict()     # get the variable dict
        for key, value in self.__var_dict.iteritems():   # Iterate through and write changes
            proceed = True
            key = key.replace(' ', '_')
            key = key.lower()
            # We want to warn users if they change the default db
            if key == 'default_database' and writing_dict[key].value() != value['value']:
                print writing_dict[key].value()
                print value['value']
                message = 'You are attempting to change the default database, are you sure sure ' \
                          'you would like to change it to %s?\n\nSelecting cancel will skip this ' \
                          'change and finish the save.' %value['value']
                proceed = tkMessageBox.askokcancel('Proceed?', message)
            if not proceed:
                continue
            # Locked values that are changed in the diaglog will still be written
            writing_dict[key].force_change(value['value'])
            writing_dict[key].change_manual(value['lock_setting'])
        logger.info('Settings saved')
        # Close the window
        self.free()

    def revert(self):
        """ Reverts any unsaved changes back to the initial values """
        self.get_variable_dict()
        self.__top_frame.destroy()
        self.__settings_entries = list()
        self.__browse_buttons = list()
        self.__lock_setting_buttons = list()
        self.__top_frame = Frame(self)
        self.__top_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.create_top_frame()
