###################################
#    Created on Jul 29, 2015
#
#    @author: Grant Mercer
#
###################################

from Tkconstants import LEFT, END, RIGHT
import tkMessageBox
from Tkinter import Toplevel, Entry, Button, BOTH, Frame, \
    Label, TOP, X, OptionMenu, StringVar

import constants
from tools.tools import center, Observer
from log.log import logger
import re


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

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.receive_advanced_search(self)


class AdvancedSearchDialog(Toplevel):
    """
    A dialog for advanced searching, notifying `ImportDialog` when search parameters have
    been chosen and entered. Uses the observer design pattern to notify ``ImportDialog``
    when the ranges have been changed from an invalid state to valid.

    :param parent: The class to attach the observer to
    :param root: The base widget for ``Toplevel``
    """

    # This dialog should be a singleton, so the caller will ensure
    # no other windows are open by checking this variable
    singleton = False

    def __init__(self, parent, root):
        AdvancedSearchDialog.singleton = True           # pseudo singleton now active
        Toplevel.__init__(self, root)

        self.title = 'Advanced search'
        self.transient(root)
        self.shared_data = Query()
        self.shared_data.attach(parent)
        self.protocol('WM_DELETE_WINDOW', self.free)

        center(self, (constants.IMADVWIDTH, constants.IMADVHEIGHT))

        window_frame = Frame(self)
        window_frame.pack(fill=BOTH, expand=True)
        top_window_frame = Frame(window_frame)
        top_window_frame.pack(side=TOP, fill=X, expand=False)
        Label(top_window_frame, text='Filter by: ').pack(side=LEFT, padx=15, pady=5)
        Label(top_window_frame, text='Leave fields untouched that you do not wish to search by',
              font=('Helvetica', 8)).pack(side=RIGHT, padx=15, pady=5)
        bottom_window_frame = Frame(window_frame)
        bottom_window_frame.pack(side=TOP, fill=BOTH, expand=False, padx=15)
        bottom_window_frame.config(highlightthickness=1)
        bottom_window_frame.config(highlightbackground='grey')
        Label(bottom_window_frame, text='Plot ').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='Date(YYYY-MM-DD) ').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='Time Range ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='Latitude Range ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='Altitude Range ').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        Label(bottom_window_frame, text='File ').grid(row=5, column=0, padx=5, pady=5, sticky='w')

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
        Label(bottom_window_frame, text='to').grid(row=3, column=2, pady=5, sticky='w')
        self.e_lat_entry = Entry(bottom_window_frame, width=10)
        self.e_lat_entry.grid(row=3, column=3, padx=5, pady=5, sticky='w')
        self.e_lat_entry.insert(END, '0.0')

        self.b_alt_entry = Entry(bottom_window_frame, width=10)
        self.b_alt_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.b_alt_entry.insert(END, '0.0')
        Label(bottom_window_frame, text='to').grid(row=4, column=2, pady=5, sticky='w')
        self.e_alt_entry = Entry(bottom_window_frame, width=10)
        self.e_alt_entry.grid(row=4, column=3, padx=5, pady=5, sticky='w')
        self.e_alt_entry.insert(END, '0.0')

        self.file_entry = Entry(bottom_window_frame, width=25)
        self.file_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w', columnspan=4)

        bottom_button_frame = Frame(window_frame)
        bottom_button_frame.pack(side=TOP, fill=BOTH, expand=False)

        Button(bottom_button_frame, text='Search', command=self.parse_ranges).\
            pack(side=LEFT, padx=15, pady=10)

    def parse_ranges(self):
        """
        Command for the search button, upon the user clicking the search button this function
        will perform a number of regex parsing to ensure all fields contain valid numbers, then
        sets the observers range dictionary to the valid fields and destroys AdvancedSearchDialog.
        If any fields are invalid, an error will be displayed and the function will return, keeping
        the window open and allowing the user to fix their error.
        """
        date = self.date_entry.get()
        r_date = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
        valid_entries = dict()
        if r_date.match(date) is None:
            logger.error('Invalid date entered \'%s\'' % date)
            tkMessageBox.showerror('Invalid field', 'Invalid date \'%s\' entered,' % date +
                                   ' must match year-mo-day format')
            return
        if date == '0000-00-00':
            date = ''
        valid_entries['date'] = date

        beg_time = self.b_time_entry.get()
        r_time = re.compile('[0-6]{2}:[0-6]{2}:[0-6]{2}')
        if r_time.match(beg_time) is None:
            logger.error('Invalid beginning time range entered \'%s\'' % beg_time)
            tkMessageBox.showerror('Invalid field', 'Invalid beginning time range' +
                                   ' \'%s\', must match hr:mn:sc format' % beg_time)
            return

        end_time = self.e_time_entry.get()
        if r_time.match(end_time) is None:
            logger.error('Invalid ending time range entered \'%s\'' % end_time)
            tkMessageBox.showerror('Invalid fieldy', 'Invalid ending time range' +
                                   ' \'%s\', must match hr:mn:sc format' % end_time)
            return

        if self.am_pm.get() == '' and (beg_time != '00:00:00' or end_time != '00:00:00'):
            logger.error('am/pm not specified but time given')
            tkMessageBox.showerror('Invalid field', 'Time entered but no am/pm specified,' +
                                   'specify whether the time is am/pm')
            return

        if end_time == '00:00:00':
            end_time = ''
        if beg_time == '00:00:00':
            beg_time = ''
        valid_entries['etime'] = end_time
        valid_entries['btime'] = beg_time

        beg_lat = self.b_lat_entry.get()
        r_lat = re.compile('[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')
        if r_lat.match(beg_lat) is None:
            logger.error('Invalid beginning lat range entered \'%s\'' % beg_lat)
            tkMessageBox.showerror('Invalid field', 'Invalid beginning latitude range' +
                                   ' \'%s\', must be a valid number(e.g. -2.3 , 4, 0.0)'
                                   % beg_lat)
            return
        if beg_lat == '0.0':
            beg_lat = ''
        valid_entries['blat'] = beg_lat

        end_lat = self.e_lat_entry.get()
        if r_lat.match(end_lat) is None:
            logger.error('Invalid ending lat range entered \'%s\'' % end_lat)
            tkMessageBox.showerror('Invalid field', 'Invalid ending latitude range' +
                                   ' \'%s\', must be valid number(e.g. -2.3, 4, 0.0'
                                   % end_lat)
            return
        if end_lat == '0.0':
            end_lat = ''
        valid_entries['elat'] = end_lat

        beg_alt = self.b_alt_entry.get()
        # r_lat is actually the same regex so we can just use that
        if r_lat.match(beg_alt) is None:
            logger.error('Invalid beginning alt range entered \'%s\'' % beg_alt)
            tkMessageBox.showerror('Invalid field', 'Invalid beginning altitude range' +
                                   ' \'%s\', must be a valid number(e.g. -2.3, 4, 0.0'
                                   % beg_alt)
            return
        if beg_alt == '0.0':
            beg_alt = ''
        valid_entries['balt'] = beg_alt

        end_alt = self.e_alt_entry.get()
        if r_lat.match(end_alt) is None:
            logger.error('Invalid ending alt range entered \'%s\'' % end_alt)
            tkMessageBox.showerror('Invalid field', 'Invalid beginning altitude range' +
                                   ' \'%s\', must be a valid number(e.g. -2.3, 4, 0.0'
                                   % end_alt)
            return
        if end_alt == '0.0':
            end_alt = ''
        valid_entries['ealt'] = end_alt

        file_ = self.file_entry.get()
        if file_ and file_.find('.hdf') == -1:
            logger.info('No extension found in file entry, appending .hdf')
            file_ += '.hdf'
        valid_entries['plot'] = self.plots.get()
        valid_entries['ampm'] = self.am_pm.get()
        valid_entries['file'] = file_

        # update ranges dictionary which will call ImportDialog receive()
        self.shared_data.ranges = valid_entries
        AdvancedSearchDialog.singleton = False
        self.destroy()

    def free(self):
        """
        Notify base class window has been destroyed.
        """
        logger.info('Closing AdvancedSearchDialog')
        AdvancedSearchDialog.singleton = False
        self.destroy()
