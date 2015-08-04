import Tkinter as tk
import ttk

class TestButton(object):

    def __init__(self, root, text):
        self.root = root
        self.text = text
        self.toggle = True
        self.style = ttk.Style()
        self.button = ttk.Button(self.root, text=self.text, command=lambda: self.push(), style='SunkableButton.TButton')
        #self.button.pack(fill=tk.BOTH, expand=True)

    def push(self):
        self.toggle = not self.toggle
        if self.toggle:
            self.button.state(['!pressed'])
            self.style.configure('SunkableButton.TButton', relief=tk.RAISED)
        else:
            self.button.state(['pressed'])
            self.style.configure('SunkableButton.TButton', relief=tk.SUNKEN)
            
    def grid(self, row, column):
        self.button.grid(row=row, column=column)

root = tk.Tk()
root.geometry('200x100')
test_button = TestButton(root, 'Test')
test_button.grid(0, 0)
another_button = TestButton(root, 'Another Button')
another_button.grid(0, 1)
other_button = TestButton(root, 'other')
other_button.grid(1, 0)
root.mainloop()