###################################
#   Created on Jun 15, 2015
#
#   @author: Grant Mercer
###################################
from Tkinter import Label, Toplevel, Frame, Button, IntVar, BOTH, FALSE, \
    BOTTOM, Radiobutton, Entry, X, TOP
from PIL import ImageTk
from tools.toggleablebutton import ToggleableButton, ToolbarToggleableButton
from tools.tooltip import create_tool_tip
from log import logger

import constants
import re
import tkMessageBox


class ToolsWindow(Toplevel):
    """
    Other main portion of the program, the tools window is in charge of managing all
    tool and manipulation related buttons , and is created bound to root but is
    technically a standalone window.

    :param parent: the class that has this instance of ToolsWindow
    :param root: the root of the program
    """
    def __init__(self, parent, root):
        Toplevel.__init__(self, root)

        # Images required by buttons
        self.test_img = ImageTk.PhotoImage(file='ico/button.png')
        self.edit_img = ImageTk.PhotoImage(file='ico/edit.png')
        self.prop_img = ImageTk.PhotoImage(file='ico/cog.png')
        self.load_img = ImageTk.PhotoImage(file='ico/load.png')
        self.save_img = ImageTk.PhotoImage(file='ico/save.png')
        self.plot_img = ImageTk.PhotoImage(file='ico/hide.png')
        self.outline_img = ImageTk.PhotoImage(file='ico/focus.png')
        self.paint_img = ImageTk.PhotoImage(file='ico/paint.png')
        self.erase_img = ImageTk.PhotoImage(file='ico/eraser.png')
        self.drag_img = ImageTk.PhotoImage(file='ico/cursorhand.png')
        self.plot_cursor_img = ImageTk.PhotoImage(file='ico/plotcursor.png')
        self.free_draw_img = ImageTk.PhotoImage(file='ico/freedraw.png')
        self.polygon_img = ImageTk.PhotoImage(file='ico/polygon.png')
        self.redo_img = ImageTk.PhotoImage(file='ico/forward.png')
        self.undo_img = ImageTk.PhotoImage(file='ico/back.png')
        self.magnify_draw_img = ImageTk.PhotoImage(file='ico/magnify.png')

        self.__parent = parent
        self.__root = root
        self.plot_type = IntVar()

        self.title('Tools')
        self.resizable(width=FALSE, height=FALSE)
        self.protocol('WM_DELETE_WINDOW', ToolsWindow.ignore)
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)

        self.coordinate_frame = Frame(self.container, width=50, height=50)
        self.coordinate_frame.config(highlightthickness=1)
        self.coordinate_frame.config(highlightbackground='grey')
        self.coordinate_frame.pack(side=BOTTOM, fill=BOTH, expand=False)

        self.upper_button_frame = None
        self.upper_range_frame = None
        self.lower_button_frame = None
        self.begin_range_entry = None
        self.end_range_entry = None

    @staticmethod
    def ignore():
        """
        Do nothing when the user presses the close button
        """
        pass

    def setup_toolbar_buttons(self):
        """
        Create tool bar buttons
        """
        logger.info('Setting up toolbar')

        self.upper_button_frame = Frame(self.container)
        self.upper_button_frame.pack(side=TOP, fill=X)

        # Reset and render button
        reset_button = Button(self.upper_button_frame, text='Reset', width=12, command=self.__parent.reset)
        reset_button.grid(row=0, column=0, pady=2)
        create_tool_tip(reset_button, 'Reset the field of view and clear polygons')
        render_button = Button(self.upper_button_frame, text='Render', width=12, height=4, command=self.render)
        render_button.grid(row=0, column=1, rowspan=4, sticky='e')
        create_tool_tip(render_button, 'Render the loaded file\nto the screen')

        # Plot selection type
        Radiobutton(self.upper_button_frame, text='Backscattered',
                    variable=self.plot_type, value=constants.BACKSCATTERED)\
            .grid(row=1, column=0, sticky='w')
        Radiobutton(self.upper_button_frame, text='Depolarized',
                    variable=self.plot_type, value=constants.DEPOLARIZED).\
            grid(row=2, column=0, sticky='w')

        self.upper_range_frame = Frame(self.container)
        self.upper_range_frame.pack(side=TOP, fill=X)

        Label(self.upper_range_frame, text='Step').\
            grid(row=3, column=0, pady=5, sticky='w')
        self.begin_range_entry = Entry(self.upper_range_frame, width=12)
        self.begin_range_entry.grid(row=3, column=1, pady=5, sticky='w')

        Label(self.upper_range_frame, text='to').\
            grid(row=3, column=2, pady=5, sticky='w')
        self.end_range_entry = Entry(self.upper_range_frame, width=11)
        self.end_range_entry.grid(row=3, column=3, pady=5, sticky='w')

        self.lower_button_frame = Frame(self.container)
        self.lower_button_frame.config(highlightthickness=1)
        self.lower_button_frame.config(highlightbackground='grey')
        self.lower_button_frame.pack(side=BOTTOM)

        Label(self.lower_button_frame, width=1).grid(row=0, column=0)
        Label(self.lower_button_frame, width=1).grid(row=0, column=5)

        # Magnify icon
        logger.info('Creating toolbar buttons')
        zoom_button = ToolbarToggleableButton(self.__root, self.lower_button_frame,
                                              lambda: self.__parent.get_toolbar().zoom(True),
                                              image=self.magnify_draw_img, width=30, height=30)
        zoom_button.latch(cursor='tcross')
        zoom_button.grid(row=0, column=2, padx=2, pady=5)
        create_tool_tip(zoom_button, 'Zoom to rect')

        # Plot undo icon
        undo_button = Button(self.lower_button_frame, image=self.undo_img, width=30, height=30,
                             command=lambda: self.__parent.get_toolbar().back(True))
        undo_button.grid(row=0, column=3, padx=2, pady=5)
        create_tool_tip(undo_button, 'Previous View')

        # Plot redo icon
        redo_button = Button(self.lower_button_frame, image=self.redo_img, width=30, height=30,
                             command=lambda: self.__parent.get_toolbar().forward(True))
        redo_button.grid(row=0, column=4, padx=2, pady=5)
        create_tool_tip(redo_button, 'Next View')

        # Draw rectangle shape
        polygon_button = \
            ToggleableButton(self.__root, self.lower_button_frame, image=self.polygon_img, width=30, height=30)
        polygon_button.latch(key='<Button-1>',
                             command=self.__parent.get_polygon_list().anchorRectangle, cursor='tcross')
        polygon_button.latch(key='<B1-Motion>',
                             command=self.__parent.get_polygon_list().rubberBand, cursor='tcross')
        polygon_button.latch(key='<ButtonRelease-1>',
                             command=self.__parent.get_polygon_list().fillRectangle, cursor='tcross')
        polygon_button.grid(row=1, column=1, padx=2, pady=5)
        create_tool_tip(polygon_button, 'Draw Rect')

        # Free form shape creation
        free_draw_button = \
            ToggleableButton(self.__root, self.lower_button_frame, image=self.free_draw_img, width=30, height=30)
        free_draw_button.latch(key='<Button-1>', command=self.__parent.get_polygon_list().plotPoint, cursor='tcross')
        free_draw_button.grid(row=1, column=3, padx=2, pady=5)
        create_tool_tip(free_draw_button, 'Free Draw')

        # Pan plot left and right
        plot_cursor_button = \
            ToggleableButton(self.__root, self.lower_button_frame, image=self.plot_cursor_img, width=30, height=30)
        plot_cursor_button.latch(key='<ButtonPress-1>', command=self.__parent.pan)
        plot_cursor_button.latch(key='<ButtonRelease-1>', command=self.__parent.render_pan)
        plot_cursor_button.latch(cursor='hand1')
        plot_cursor_button.grid(row=0, column=1, padx=2, pady=5)
        create_tool_tip(plot_cursor_button, 'Move about plot')

        # Move polygon and rectangles around
        drag_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.drag_img, width=30, height=30)
        drag_button.latch(key='<Button-2>', command=self.__parent.get_polygon_list().toggleDrag, cursor='hand1')
        drag_button.grid(row=1, column=2, padx=2, pady=5)
        create_tool_tip(drag_button, 'Drag')

        # Erase polygon drawings
        erase_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.erase_img, width=30, height=30)
        erase_button.latch(key='<Button-1>', command=self.__parent.get_polygon_list().delete, cursor='X_cursor')
        erase_button.grid(row=1, column=4, padx=2, pady=5)
        create_tool_tip(erase_button, 'Erase polygon')

        # Recolor shapes
        paint_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.paint_img, width=30, height=30)
        paint_button.latch(key='<Button-1>', command=self.__parent.get_polygon_list().paint, cursor='')
        paint_button.grid(row=2, column=2, padx=2, pady=5)
        create_tool_tip(paint_button, 'Paint')

        # Outline shapes
        outline_button = \
            Button(self.lower_button_frame, image=self.outline_img, width=30, height=30,
                   command=lambda: self.__parent.get_polygon_list().outline())
        outline_button.grid(row=2, column=1, padx=2, pady=5)
        create_tool_tip(outline_button, 'Focus')

        # Hide shapes
        plot_button = \
            Button(self.lower_button_frame, image=self.plot_img, width=30, height=30,
                   command=lambda: self.__parent.get_polygon_list().hide())
        plot_button.grid(row=2, column=3, padx=2, pady=5)
        create_tool_tip(plot_button, 'Hide polygons')

        # Save shapes as JSON
        save_button = \
            Button(self.lower_button_frame, image=self.save_img, width=30, height=30, command=self.__parent.save_json)
        save_button.grid(row=2, column=4, padx=2, pady=5)
        create_tool_tip(save_button, 'Save visible\n objects\n to JSON')

        # Load shapes from JSON
        load_button = \
            Button(self.lower_button_frame, image=self.load_img, width=30, height=30, command=self.__parent.load)
        load_button.grid(row=3, column=1, padx=2, pady=5)
        create_tool_tip(load_button, 'Load JSON')

        # Retrieve shape properties
        properties_button = \
            ToggleableButton(self.__root, self.lower_button_frame, image=self.prop_img, width=30, height=30)
        properties_button.latch(key='<Button-1>', command=self.__parent.get_polygon_list().properties)
        properties_button.grid(row=3, column=2, padx=2, pady=5)
        create_tool_tip(properties_button, 'Polygon Properties')

        # Edit shape attributes
        edit_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.edit_img, width=30, height=30)
        edit_button.latch(key='<Button-1>', command=self.__parent.attribute_window)
        edit_button.grid(row=3, column=3, padx=2, pady=5)
        create_tool_tip(edit_button, 'Edit Attributes')

        # Testing button
        test_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.test_img, width=30, height=30)
        test_button.latch(key='<Button-1>', command=self.__parent.get_polygon_list().extractShapeData)
        test_button.grid(row=3, column=4, padx=2, pady=5)
        create_tool_tip(test_button, 'test button')

    def render(self):
        """
        Errors checks all user entered parameters and calls ``set_plot`` from *Calipso*
        """
        logger.info('Grabbing range and safe checking')
        if self.plot_type.get() == 0:
            logger.error('No plot type set')
            tkMessageBox.showerror('toolswindow', 'No plot type specified')
            return

        # default beginning and ending range
        beginning_range = 0
        ending_range = 1000

        # If entry has text
        if self.begin_range_entry.get():
            # If entry is not ONLY numbers
            if not re.match('[0-9]+', self.begin_range_entry.get()) or '.' in self.begin_range_entry.get():
                logger.error('Beginning range invalid, not all numeric')
                tkMessageBox.showerror('toolswindow',
                                       'Invalid beginning range, range must only contain digits')
                return
            # default ending range is beginning_range + 1000
            beginning_range = int(self.begin_range_entry.get())
            ending_range = beginning_range + 1000
        # If entry as text
        if self.end_range_entry.get():
            # If entry is not ONLY numbers
            if not re.match('[0-9]+', self.end_range_entry.get()) or '.' in self.end_range_entry.get():
                logger.error('Ending range invalid, not all numeric')
                tkMessageBox.showerror('toolswindow',
                                       'Invalid ending range, range must only contain digits')
                return
            ending_range = int(self.end_range_entry.get())

        if beginning_range > ending_range:
            logger.error('Beginning range larger than ending range %d > %d' % (beginning_range, ending_range))
            tkMessageBox.showerror('toolswindow',
                                   'Beginning range cannot be larger than ending range')
            return

        # If any negative values or the step is too small
        if beginning_range < 0 or ending_range < 0 or ending_range - beginning_range < 100:
            logger.error('Error, invalid range specifiers %d , %d' % (beginning_range, ending_range))
            tkMessageBox.showerror('toolswindow',
                                   'Range cannot be less than zero or smaller than 100 steps')
            return

        logger.info('Calling plot')
        self.__parent.set_plot(self.plot_type.get(), xrange_=(beginning_range, ending_range))
