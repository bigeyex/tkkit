import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import threading

class Widget:
    # override if there's additional arguments
    def __init__(self, name=None, **kwargs):
        self.styles = kwargs
        self.name = name

    def bind_var(self): # override if there's binding variable, none for skipping
        return None
    
    def get_value(self):
        return self.var_to_bind.get()
    
    def set_value(self, value):
        self.var_to_bind.set(value)

    def show(self, parent): # should never be overridden
        self.name_registry = parent.name_registry
        self.parent = parent
        self.var_to_bind = self.bind_var()
        if self.name is not None and self.name not in self.name_registry:
            self.name_registry[self.name] = self
        self.el = self.get_widget(parent)
        return self.el

    def get_widget(self, parent):
        raise NotImplementedError('get_widget is not implemented')


class Column(Widget):
    def __init__(self, children=[], name=None, **kwargs):
        self.children = children
        super().__init__(name=name, **kwargs)
    
    def get_widget(self, parent):
        self.el = tk.Frame(parent.el, **self.styles)
        for index in range(0, len(self.children)):
            child_el = self.children[index].show(self)
            child_el.grid(row=index, column=0)
        return self.el
            
class Row(Column):
    def get_widget(self, parent):
        self.el = tk.Frame(parent.el, **self.styles)
        for index in range(0, len(self.children)):
            child_el = self.children[index].show(self)
            child_el.grid(row=0, column=index)
        return self.el

class Window(Column):
    pass

class Button(Widget):
    def __init__(self, text="Button", name=None, on_click=None, **kwargs):
        self.text = text
        self.on_click = on_click
        super().__init__(name=name, **kwargs)

    def handle_click(self):
        handler_thread = threading.Thread(target=self.on_click, daemon=True)
        handler_thread.start()

    def get_widget(self, parent):
        command = self.handle_click if self.on_click is not None else None
        return ttk.Button(parent.el, text=self.text, command=command, **self.styles)
    
class Label(Widget):
    def __init__(self, text="Label", name=None, **kwargs):
        self.text = text
        super().__init__(name=name, **kwargs)

    def get_widget(self, parent):
        return ttk.Label(parent.el, text=self.text, **self.styles)
    
class TextBox(Widget):
    def __init__(self, text="", password=False, lines=1, scrollable=True, name=None, **kwargs):
        self.text = text
        self.password = password
        self.lines = lines
        self.scrollable = scrollable
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        return tk.StringVar()
    
    def get_value(self):
        if self.lines > 1:
            return self.el.get('1.0', 'end')
        else:
            return self.var_to_bind.get()
        
    def set_value(self, value):
        if self.lines > 1:
            self.el.delete(1.0, 'end')
            self.el.insert("end", value)
        else:
            self.var_to_bind.set(value)

    def get_widget(self, parent):
        show = '*' if self.password else None
        if self.text is not None and self.var_to_bind is not None:
            self.var_to_bind.set(self.text)
        if self.lines > 1:
            if self.scrollable:
                return ScrolledText(parent.el, height=self.lines, **self.styles)
            else:
                return tk.Text(parent.el, height=self.lines, **self.styles)
        else:
            return ttk.Entry(parent.el, textvariable=self.var_to_bind, show=show, **self.styles)

class CheckBox(Widget):
    def __init__(self, text="CheckBox", name=None, checked=False, on_click=None, **kwargs):
        self.text = text
        self.on_click = on_click
        self.checked = checked
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        var_to_bind = tk.IntVar()
        if self.checked:
            var_to_bind.set(1)
        return var_to_bind
    
    def get_value(self):
        return self.var_to_bind.get() == 1
    
    def set_value(self, value):
        self.var_to_bind.set(value == 1)

    def get_widget(self, parent):
        return ttk.Checkbutton(parent.el, text=self.text, command=self.on_click, variable=self.var_to_bind, **self.styles)
    
class RadioButton(Widget):
    def __init__(self, text="RadioButton", value=None, name=None, selected=False, on_click=None, **kwargs):
        if value is None:
           value = text 
        self.text = text
        self.on_click = on_click
        self.value = value
        self.selected = selected
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        if self.name not in self.name_registry or self.name_registry[self.name].var_to_bind is None:
            var_to_bind = tk.StringVar()
        else:
            var_to_bind = self.name_registry[self.name].var_to_bind
        if self.selected:
            var_to_bind.set(self.value)
        return var_to_bind

    def get_widget(self, parent):
        return ttk.Radiobutton(parent.el, text=self.text, value=self.value, command=self.on_click, variable=self.var_to_bind, **self.styles)
    
class ComboBox(Widget):
    def __init__(self, values=(), name=None, selected=None, on_change=None, **kwargs):
        self.values = values
        self.on_change = on_change
        self.selected = selected
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        return tk.StringVar(value=self.selected)

    def get_widget(self, parent):
        widget = ttk.Combobox(parent.el, values=self.values, textvariable=self.var_to_bind, **self.styles)
        if self.on_change is not None:
            widget.bind('<<ComboboxSelected>>', lambda val:self.on_change())
        return widget
    
class ListBox(Widget):
    def __init__(self, values=(), name=None, lines=5, selected=None, multiple=False, on_change=None, **kwargs):
        self.values = values
        self.on_change = on_change
        self.selected = selected
        self.lines = lines
        self.multiple = multiple
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        return tk.StringVar(value=self.values)
    
    def get_value(self):
        selected_indices = self.el.curselection()
        if self.multiple:
            return [self.el.get(i) for i in selected_indices]
        else:
            return self.el.get(selected_indices[0])
    
    def set_value(self, value):
        for i in range(len(self.values)):
            if self.multiple and self.values[i] in value:
                self.el.selection_set(i)
            elif not self.multiple and self.values[i] == value:
                self.el.selection_set(i)
            else:
                self.el.selection_clear(i)

    def get_widget(self, parent):
        select_mode = tk.EXTENDED if self.multiple else tk.BROWSE
        widget = tk.Listbox(parent.el, height=self.lines, listvariable=self.var_to_bind, selectmode=select_mode, **self.styles)
        if self.on_change is not None:
            widget.bind('<<ListboxSelect>>', lambda val:self.on_change())
        return widget