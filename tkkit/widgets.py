from tkinter import *
from tkinter import ttk

class Widget:
    pass


class Column(Widget):
    def __init__(self, children=[], **kwargs):
        self.children = children
        self.styles = kwargs
    
    def show(self, parent):
        frame = Frame(parent, **self.styles)
        for index in range(0, len(self.children)):
            child_el = self.children[index].show(self)
            child_el.grid(row=index, column=0)
        return frame
            
class Row(Column):
    def show(self, parent):
        frame = Frame(parent, **self.styles)
        for index in range(0, len(self.children)):
            child_el = self.children[index].show(self)
            child_el.grid(row=0, column=index)
        return frame

class Window(Column):
    pass

class Button(Widget):
    pass