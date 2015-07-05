######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################

class ShapeManager(object):
    """
    Manages all shapes present on the screen, writes to database on
    call and provides other export functionality
    """

    outline_toggle = True
    hide_toggle = True

    def __init__(self, canvas, master):
        pass

    def on_token_buttonpress(self, event):
        pass

    def on_token_buttonrelease(self, event):
        pass

    def on_token_motion(self, event):
        pass

    def set_plot(self, plot):
        pass

    def anchor_rectangle(self, event):
        pass

    def get_count(self):
        pass

    def get_filename(self):
        pass

    def plot_point(self, event):
        pass

    def rubberband(self, event):
        pass

    def fill_rectangle(self, event):
        pass

    def set_hdf(self, hdf_filename):
        pass

    def draw(self):
        pass

    def generate_tag(self, index=-1):
        pass

    def reset(self):
        pass

    def delete(self, event):
        pass

    def outline(self):
        pass

    def paint(self, event):
        pass

    def hide(self):
        pass

    def properties(self, event):
        pass

    def toggle_drag(self, event):
        pass

    def find_shape(self, event):
        pass

    def __find_shape_by_itemhandler(self, itemhandler):
        pass

    @staticmethod
    def __plot_into_string(plot):
        pass

    @staticmethod
    def plot_string_to_int(plot):
        pass

    def read_plot(self, filename='', read_from_str=''):
        pass

    def save_db(self):
        pass

    def save_json(self, filename=''):
        pass

    def save_all_json(self, filename):
        pass