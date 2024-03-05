from tkinter import *
from tkinter import ttk

class TKApp:
    def __init__(self, title=None):
        self.root = Tk()
        if title is None:
            self.root.title(title)

    def show(self, window):
        self.name_registry = {}
        window.show(self)

    def run(self):
        self.root.mainloop()
