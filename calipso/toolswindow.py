###################################
#   Created on Jun 15, 2015
#
#   @author: Grant Mercer
###################################
from Tkconstants import END
from Tkinter import Label, Toplevel, Frame, Button, IntVar, BOTH, FALSE, \
    BOTTOM, Radiobutton, Entry, X, TOP
import re
import tkMessageBox

from PIL import ImageTk
from constants import Plot, PATH
from log.log import logger
from tools.toggleablebutton import ToggleableButton, ToolbarToggleableButton
from tools.tooltip import create_tool_tip


class ToolsWindow(Toplevel):
    """
    Other main portion of the program, the tools window is in charge of managing all
    tool and manipulation related buttons , and is created bound to root but is
    technically a standalone window.

    :param parent: the class that has this instance of ToolsWindow
    :param root: the root of the program
    """
    def __init__(self, canvas, parent, root):
        Toplevel.__init__(self, root)
        # Images required by buttons
        self.edit_img = ImageTk.PhotoImage(file=PATH + '/ico/edit.png')
        self.prop_img = ImageTk.PhotoImage(file=PATH + '/ico/cog.png')
        self.load_img = ImageTk.PhotoImage(file=PATH + '/ico/load.png')
        self.save_img = ImageTk.PhotoImage(file=PATH + '/ico/save.png')
        self.plot_img = ImageTk.PhotoImage(file=PATH + '/ico/hide.png')
        self.outline_img = ImageTk.PhotoImage(file=PATH + '/ico/focus.png')
        self.paint_img = ImageTk.PhotoImage(file=PATH + '/ico/paint.png')
        self.erase_img = ImageTk.PhotoImage(file=PATH + '/ico/eraser.png')
        self.drag_img = ImageTk.PhotoImage(file=PATH + '/ico/cursorhand.png')
        self.plot_cursor_img = ImageTk.PhotoImage(file=PATH + '/ico/plotcursor.png')
        self.free_draw_img = ImageTk.PhotoImage(file=PATH + '/ico/freedraw.png')
        self.polygon_img = ImageTk.PhotoImage(file=PATH + '/ico/polygon.png')
        self.redo_img = ImageTk.PhotoImage(file=PATH + '/ico/forward.png')
        self.undo_img = ImageTk.PhotoImage(file=PATH + '/ico/back.png')
        self.magnify_draw_img = ImageTk.PhotoImage(file=PATH + '/ico/magnify.png')
        self.extract_img = ImageTk.PhotoImage(file=PATH + '/ico/extract.png')
        self.home_img = ImageTk.PhotoImage(file=PATH + '/ico/home.png')

        self.__parent = parent
        self.__root = root
        self.__canvas = canvas
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
        self.begin_alt_range_entry = None
        self.end_range_entry = None
        self.end_alt_range_entry = None

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
        #self.upper_button_frame.pack(side=TOP, fill=X)
        self.upper_button_frame.grid(0, 0)

        # Reset and render button
        reset_button = Button(self.upper_button_frame, text='Reset', width=12, command=self.__parent.reset)
        reset_button.grid(row=0, column=0, pady=2)
        create_tool_tip(reset_button, 'Reset the field of view and clear polygons')
        render_button = Button(self.upper_button_frame, text='Render', width=12, height=4, command=self.render)
        render_button.grid(row=0, column=1, rowspan=4, sticky='e')
        create_tool_tip(render_button, 'Render the loaded file\nto the screen')

        # Plot selection type
        Radiobutton(self.upper_button_frame, text='Backscattered',
                    variable=self.plot_type, value=Plot.backscattered)\
            .grid(row=1, column=0, sticky='w')
        Radiobutton(self.upper_button_frame, text='Depolarized',
                    variable=self.plot_type, value=Plot.depolarized).\
            grid(row=2, column=0, sticky='w')

        self.upper_range_frame = Frame(self.container)
        self.upper_range_frame.pack(side=TOP, fill=X)

        Label(self.upper_range_frame, text='Step').\
            grid(row=3, column=0, pady=5, sticky='w')
        self.begin_range_entry = Entry(self.upper_range_frame, width=12)
        self.begin_range_entry.grid(row=3, column=1, pady=5, sticky='w')
        self.begin_range_entry.insert(END, '0')

        Label(self.upper_range_frame, text='to').\
            grid(row=3, column=2, pady=5, sticky='w')
        self.end_range_entry = Entry(self.upper_range_frame, width=11)
        self.end_range_entry.grid(row=3, column=3, pady=5, sticky='w')
        self.end_range_entry.insert(END, '1000')

        Label(self.upper_range_frame, text='Alt').\
            grid(row=4, column=0, pady=5, sticky='w')
        self.begin_alt_range_entry = Entry(self.upper_range_frame, width=12)
        self.begin_alt_range_entry.grid(row=4, column=1, pady=5, sticky='w')
        self.begin_alt_range_entry.insert(END, '0')

        Label(self.upper_range_frame, text='to').\
            grid(row=4, column=2, pady=5, sticky='w')
        self.end_alt_range_entry = Entry(self.upper_range_frame, width=11)
        self.end_alt_range_entry.grid(row=4, column=3, pady=5, sticky='w')
        self.end_alt_range_entry.insert(END, '20')

        self.lower_button_frame = Frame(self.container)
        self.lower_button_frame.config(highlightthickness=1)
        self.lower_button_frame.config(highlightbackground='grey')
        self.lower_button_frame.pack(side=BOTTOM)

        Label(self.lower_button_frame, width=1).grid(row=0, column=0)
        Label(self.lower_button_frame, width=1).grid(row=0, column=5)
        
        # Pan plot left and right
        plot_cursor_button = \
            ToggleableButton(self.__root, self.lower_button_frame, image=self.plot_cursor_img, width=30, height=30)
        plot_cursor_button.latch(target=self.__canvas, key='button_press_event', 
                                 command=self.__parent.pan)
        plot_cursor_button.latch(target=self.__canvas, key='button_release_event', 
                                 command=self.__parent.render_pan)
        plot_cursor_button.latch(cursor='hand1')
        plot_cursor_button.grid(row=0, column=1, padx=2, pady=5)
        create_tool_tip(plot_cursor_button, 'Move about plot')

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

        # Home button
        home_button = Button(self.lower_button_frame, image=self.home_img,
                             command=lambda: self.__parent.get_toolbar().home(),
                             width=30, height=30)
        home_button.grid(row=1, column=1, padx=2, pady=5)
        create_tool_tip(home_button, 'Home')

        # Retrieve shape properties
        properties_button = \
            ToggleableButton(self.__root, self.lower_button_frame, image=self.prop_img, width=30, height=30)
        properties_button.latch(target=self.__canvas, key='pick_event',
                                command=self.__parent.get_shapemanager().properties)
        properties_button.grid(row=1, column=2, padx=2, pady=5)
        create_tool_tip(properties_button, 'Polygon Properties')

        # Edit shape attributes
        edit_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.edit_img, width=30, height=30)
        edit_button.latch(target=self.__canvas, key='pick_event',
                          command=self.__parent.attribute_window)
        edit_button.grid(row=1, column=3, padx=2, pady=5)
        create_tool_tip(edit_button, 'Edit Attributes')

        # Extract data
        extract_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.extract_img, width=30, height=30)
        extract_button.latch(target=self.__canvas, key='pick_event',
                             command=self.__parent.extract_window)
        extract_button.grid(row=1, column=4, padx=2, pady=5)
        create_tool_tip(extract_button, 'Extract data from shape')

        # Draw rectangle shape
        polygon_button = \
            ToggleableButton(self.__root, self.lower_button_frame, image=self.polygon_img, width=30, height=30)
        polygon_button.latch(target=self.__canvas,
                             key='button_press_event',
                             command=self.__parent.get_shapemanager().anchor_rectangle, cursor='tcross')
        polygon_button.latch(target=self.__canvas,
                             key='motion_notify_event',
                             command=self.__parent.get_shapemanager().rubberband)
        polygon_button.latch(target=self.__canvas,
                             key='button_release_event',
                             command=self.__parent.get_shapemanager().fill_rectangle, cursor='tcross')
        polygon_button.grid(row=2, column=1, padx=2, pady=5)
        create_tool_tip(polygon_button, 'Draw Rect')

        # Free form shape creation
        free_draw_button = \
            ToggleableButton(self.__root, self.lower_button_frame, image=self.free_draw_img, width=30, height=30)
        free_draw_button.latch(target=self.__canvas, key='button_press_event', 
                               command=self.__parent.get_shapemanager().plot_point, cursor='tcross',
                               destructor=self.__parent.get_shapemanager().clear_lines)
        free_draw_button.grid(row=2, column=2, padx=2, pady=5)
        create_tool_tip(free_draw_button, 'Free Draw')
        
        # Erase polygon drawings
        erase_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.erase_img, width=30, height=30)
        erase_button.latch(target=self.__canvas, key='pick_event',
                           command=self.__parent.get_shapemanager().delete, 
                           cursor='X_cursor')
        erase_button.grid(row=2, column=3, padx=2, pady=5)
        create_tool_tip(erase_button, 'Erase polygon')
        
        # Recolor shapes
        paint_button = ToggleableButton(self.__root, self.lower_button_frame, image=self.paint_img, width=30, height=30)
        paint_button.latch(target=self.__canvas, key='pick_event',
                           command=self.__parent.paint_window,
                           cursor='')
        paint_button.grid(row=2, column=4, padx=2, pady=5)
        create_tool_tip(paint_button, 'Paint')
        
        # Outline shapes
        outline_button = \
            Button(self.lower_button_frame, image=self.outline_img, width=30, height=30,
                   command=lambda: self.__parent.get_shapemanager().outline())
        outline_button.grid(row=3, column=1, padx=2, pady=5)
        create_tool_tip(outline_button, 'Focus')

        # Hide shapes
        plot_button = \
            Button(self.lower_button_frame, image=self.plot_img, width=30, height=30,
                   command=lambda: self.__parent.get_shapemanager().hide())
        plot_button.grid(row=3, column=2, padx=2, pady=5)
        create_tool_tip(plot_button, 'Hide polygons')

        # Save shapes as JSON
        save_button = \
            Button(self.lower_button_frame, image=self.save_img, width=30, height=30, command=self.__parent.save_json)
        save_button.grid(row=3, column=3, padx=2, pady=5)
        create_tool_tip(save_button, 'Save visible\n objects\n to JSON')
        
        # Load shapes from JSON
        load_button = \
            Button(self.lower_button_frame, image=self.load_img, width=30, height=30, command=self.__parent.load)
        load_button.grid(row=3, column=4, padx=2, pady=5)
        create_tool_tip(load_button, 'Load JSON')

    @staticmethod
    def __check_range(beginning_range, ending_range, min_range,
                      begin_range_entry, end_range_entry):
        # If entry has text
        if begin_range_entry.get():
            # If entry is not ONLY numbers
            if not re.match('[0-9]+', begin_range_entry.get()) or '.' in begin_range_entry.get():
                logger.error('Beginning range invalid, not all numeric')
                tkMessageBox.showerror('toolswindow',
                                       'Invalid beginning range, range must only contain digits')
                return None
            # default ending range is beginning_range + 1000
            beginning_range = int(begin_range_entry.get())
            ending_range = beginning_range + 1000
        # If entry as text
        if end_range_entry.get():
            # If entry is not ONLY numbers
            if not re.match('[0-9]+', end_range_entry.get()) or '.' in end_range_entry.get():
                logger.error('Ending range invalid, not all numeric')
                tkMessageBox.showerror('toolswindow',
                                       'Invalid ending range, range must only contain digits')
                return None
            ending_range = int(end_range_entry.get())

        if beginning_range > ending_range:
            logger.error('Beginning range larger than ending range %d > %d' % (beginning_range, ending_range))
            tkMessageBox.showerror('toolswindow',
                                   'Beginning range cannot be larger than ending range')
            return None

        # If any negative values or the step is too small
        if beginning_range < 0 or ending_range < 0 or ending_range - beginning_range < min_range:
            logger.error('Error, invalid range specifiers %d , %d' % (beginning_range, ending_range))
            tkMessageBox.showerror('toolswindow',
                                   'Range cannot be less than zero or smaller than 100 steps')
            return None

        if ending_range - beginning_range > 15000:
            logger.error('Error, specified range %d , %d is too large' % (beginning_range, ending_range))
            tkMessageBox.showerror('toolswindow', 'Range cannot be greater than 15000 steps')
            return None

        return beginning_range, ending_range

    def render(self):
        """
        Errors checks all user entered parameters and calls ``set_plot`` from *Calipso*
        """
        if self.plot_type.get() == 0:
            logger.error('No plot type set')
            tkMessageBox.showerror('toolswindow', 'No plot type specified')
            return

        if not self.__parent.get_file():
            logger.error('No file entered')
            tkMessageBox.showerror('toolswindow', 'No file loaded')
            return

        time_range = ToolsWindow.__check_range(0, 1000, 100,
                                               self.begin_range_entry,
                                               self.end_range_entry)
        alt_range = ToolsWindow.__check_range(0, 20, 5,
                                              self.begin_alt_range_entry,
                                              self.end_alt_range_entry)

        logger.info('Grabbing range and safe checking')
        if time_range is None or alt_range is None:
            return

        logger.info('Calling plot')
        self.__parent.set_plot(self.plot_type.get(),
                               xrange_=time_range, yrange=alt_range)
