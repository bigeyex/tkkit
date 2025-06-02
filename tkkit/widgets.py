from typing import Self
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from tkinter import filedialog 
import threading
from functools import reduce
from .view_model import ViewModelBindable
from typing import Self, List, Any, Optional
from .view_model import ViewModelBindable, BindedListUpdateType

def get_sticky(align:str, vertical_align:str):
    """
    Returns the sticky value(wsne) for the align value ("left", "right", "fill")"""
    align_table = {'left': 'w', 'right': 'e', 'fill': 'we'}
    vertical_align_table = {'top': 'n', 'bottom': 's', 'fill': 'ns'}
    sticky = align_table[align] if align in align_table else ''
    sticky = sticky + (vertical_align_table[vertical_align] if vertical_align in vertical_align_table else '')
    if sticky == '':
        return None
    else:
        return sticky

class Widget:
    # override if there's additional arguments
    def __init__(self, name:str=None, align=None, vertical_align=None, expand=0, padding=(0, 0), **kwargs):
        self.styles = kwargs
        self.align = align
        self.vertical_align = vertical_align
        self.expand = expand
        self.name:str = name
        self.padding:str = padding
        self.el:tk.Widget = None
        if isinstance(padding, int): # padding could be int, or (int, int) as (padx, pady)
            self.padding = (padding, padding)

    def bind_var(self): # override if there's binding variable, none for skipping
        return None
    
    def get_value(self):
        return self.var_to_bind.get()
    
    def set_value(self, value):
        self.var_to_bind.set(value)

    def post_container_build(self):
        pass

    def build(self, parent:Self) -> tk.Widget: # should never be overridden
        self.name_registry = parent.name_registry
        if self.align is None and parent.align != 'fill':
            self.align = parent.align
        if self.vertical_align is None and parent.align != 'fill':
            self.vertical_align = parent.vertical_align
        self.parent = parent
        self.var_to_bind = self.bind_var()
        if self.name is not None and self.name not in self.name_registry:
            self.name_registry[self.name] = self
        self.el = self.layout_tk_widget(parent)
        return self.el

    def layout_tk_widget(self, parent) -> tk.Widget:
        raise NotImplementedError('layout_tk_widget is not implemented')

class WrapperWidget(Widget):
    def __init__(self, children, **kwargs):
        self.children = children
        super().__init__(**kwargs)

class Container(Widget):
    def __init__(self, children=None, expand=1, align='fill', name=None, gap=0, **kwargs):
        self.children = children
        self.gap = gap
        super().__init__(name=name, expand=expand, align=align, **kwargs)

    def build(self, parent:Self) -> tk.Widget:
        super().build(parent)
        for child in self.children:
            child.post_container_build()
        return self.el

    def get_real_children(self):
        def reduce_children(acc, child):
            if isinstance(child, WrapperWidget):
                acc.extend(child.children)
            else:
                acc.append(child)
            return acc
        return reduce(reduce_children, self.children, [])

class Column(Container):
    def layout_tk_widget(self, parent):
        self.el = tk.Frame(parent.el, **self.styles)
        self.el.columnconfigure(0, weight=1)
        for index, child in enumerate(self.get_real_children()):
            if child.expand != 0:
                self.el.rowconfigure(index, weight=child.expand)
            padding = child.padding
            child_el = child.build(self)
            child_el.grid(row=index, column=0, padx=int(padding[1]+self.gap/2), pady=int(padding[0]+self.gap/2),
                          sticky=get_sticky(child.align, child.vertical_align))
        return self.el
            
class Row(Container):
    def __init__(self, children=None, expand=0, align='fill', name=None, **kwargs):
        super().__init__(children, expand=expand, align=align, name=name, **kwargs)

    def layout_tk_widget(self, parent):
        self.el = tk.Frame(parent.el, **self.styles)
        self.el.rowconfigure(0, weight=1)
        for index, child in enumerate(self.get_real_children()):
            child_el = child.build(self)
            if child.expand != 0:
                self.el.columnconfigure(index, weight=child.expand)
            padding = child.padding
            child_el.grid(row=0, column=index, padx=int(padding[1]+self.gap/2), pady=int(padding[0]+self.gap/2),
                          sticky=get_sticky(child.align, child.vertical_align))
        return self.el

class Window(Column):
    pass

class VStack(Column):
    pass

class HStack(Row):
    pass

class Button(Widget):
    def __init__(self, text="Button", name=None, on_click=None, **kwargs):
        if isinstance(text, ViewModelBindable):
            text.on_change(lambda value: self.el.config(text=value))
            self.text = text.get_value()
        else:
            self.text = text
        self.on_click = on_click
        super().__init__(name=name, **kwargs)

    def handle_click(self):
        handler_thread = threading.Thread(target=self.on_click, daemon=True)
        handler_thread.start()

    def layout_tk_widget(self, parent):
        command = self.handle_click if self.on_click is not None else None
        return ttk.Button(parent.el, text=self.text, command=command, **self.styles)
    
class Label(Widget):
    def __init__(self, text="Label", name=None, **kwargs):
        self.text = text
        super().__init__(name=name, **kwargs)

    def layout_tk_widget(self, parent):
        if isinstance(self.text, ViewModelBindable):
            self.text.on_change(lambda value: self.el.config(text=value))
            self.text = self.text.get_value()
        return ttk.Label(parent.el, text=self.text, **self.styles)
    
class TextBox(Widget):
    def __init__(self, text="", password=False, lines=1, scrollable=True, name=None, **kwargs):
        self.text = text
        self.password = password
        self.lines = lines
        self.scrollable = scrollable
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        var_to_bind = tk.StringVar()
        if isinstance(self.text, ViewModelBindable):
            var_to_bind.set(self.text.get_value())
            self.text.connect_tk_var(var_to_bind)
            self.text = self.text.get_value()
        return var_to_bind
    
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

    def layout_tk_widget(self, parent):
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
        if isinstance(self.checked, ViewModelBindable):
            var_to_bind.set(self.checked.get_value())
            self.checked.connect_tk_var(var_to_bind, true_to_one=True)
            self.checked = self.checked.get_value()
        elif self.checked:
            var_to_bind.set(1)
        return var_to_bind
    
    def get_value(self):
        return self.var_to_bind.get() == 1
    
    def set_value(self, value):
        self.var_to_bind.set(value == 1)

    def layout_tk_widget(self, parent):
        return ttk.Checkbutton(parent.el, text=self.text, command=self.on_click, variable=self.var_to_bind, **self.styles)
    
class RadioGroup(WrapperWidget):
    def __init__(
        self,
        children: List[Widget],
        value: Optional[Any] = None,
        on_change: Optional[callable] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        self._value = value
        self.on_change = on_change
        super().__init__(children, name=name, **kwargs)

        # Check if value is bindable
        if isinstance(self._value, ViewModelBindable):
            self._value.on_change(self._update_selection_from_bindable)

        # Set up the variable shared by all radio buttons
        self.var_to_bind = tk.StringVar()
        if isinstance(self._value, ViewModelBindable):
            self.var_to_bind.set(self._value.get_value())
        elif self._value is not None:
            self.var_to_bind.set(self._value)

        # Configure each radio button
        for child in self.children:
            if isinstance(child, RadioButton):
                child.var_to_bind = self.var_to_bind
                child.bind_var = lambda: self.var_to_bind

        self.var_to_bind.trace_add("write", self._handle_selection_change)

    def _update_selection_from_bindable(self, new_value):
        """Update the selected radio button based on the bindable value."""
        self.var_to_bind.set(new_value)

    def _handle_selection_change(self, *args):
        """Handle the selection change event and call the on_change callback."""
        new_value = self.var_to_bind.get()
        if isinstance(self._value, ViewModelBindable):
            self._value.set_value(new_value)
        if self.on_change:
            self.on_change(new_value)

    def get_value(self):
        """Get the currently selected value."""
        return self.var_to_bind.get()

    def set_value(self, value):
        """Set the selected radio button by value."""
        self.var_to_bind.set(value)

    def layout_tk_widget(self, parent):
        self.parent = parent
        self.name_registry = parent.name_registry
        frame = tk.Frame(parent.el, **self.styles)
        for child in self.children:
            child_el = child.build(self)
            child_el.pack(anchor='w')
        self.el = frame
        return self.el


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

    def layout_tk_widget(self, parent):
        return ttk.Radiobutton(
            parent.el,
            text=self.text,
            value=self.value,
            command=self.on_click,
            variable=self.var_to_bind,
            **self.styles
        )


class ComboBox(Widget):
    def __init__(self, values=(), selected=None, name=None, on_change=None, **kwargs):
        self.values = values
        self.on_change = on_change
        self.selected = selected
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        var_to_bind = tk.StringVar(value=self.selected)
        if isinstance(self.selected, ViewModelBindable):
            var_to_bind.set(self.selected.get_value())
            self.selected.connect_tk_var(var_to_bind)
            self.selected = self.selected.get_value()
        return var_to_bind

    def layout_tk_widget(self, parent):
        widget = ttk.Combobox(parent.el, values=self.values, textvariable=self.var_to_bind, **self.styles)
        if self.on_change is not None:
            widget.bind('<<ComboboxSelected>>', lambda val:self.on_change())
        return widget
    
class ListBox(Widget):
    def __init__(self, list_items=(), value=None, lines=5, multiple=False, name=None, on_change=None, **kwargs):
        self.list_items = list_items
        self.value_binder = None
        self.on_change = on_change
        self.value = value
        self.lines = lines
        self.multiple = multiple
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        if isinstance(self.value, ViewModelBindable):
            self.value_binder = self.value
            self.value_binder.on_change(lambda v: self.set_value(v))
            self.value = self.value.get_value()

        var_to_bind = tk.StringVar()
        if isinstance(self.list_items, ViewModelBindable):
            var_to_bind.set(self.list_items.get_value())
            self.list_items.connect_tk_var(var_to_bind)
            self.list_items = self.list_items.get_value()
        else:
            var_to_bind.set(self.list_items)
        return var_to_bind
    
    def get_value(self):
        selected_indices = self.el.curselection()
        if self.multiple:
            return [self.el.get(i) for i in selected_indices]
        else:
            return self.el.get(selected_indices[0])
    
    def set_value(self, value):
        for i, list_item in enumerate(self.list_items):
            if self.multiple and list_item in value:
                self.el.selection_set(i)
            elif not self.multiple and list_item == value:
                self.el.selection_set(i)
            else:
                self.el.selection_clear(i)

    def layout_tk_widget(self, parent):
        select_mode = tk.EXTENDED if self.multiple else tk.BROWSE
        self_el = tk.Listbox(parent.el, height=self.lines, listvariable=self.var_to_bind, selectmode=select_mode, **self.styles)
        def on_selected():
            if self.value_binder is not None:
                self.value_binder.set_value(self.get_value())
            self.on_change()
        if self.on_change is not None:
            self_el.bind('<<ListboxSelect>>', lambda val:on_selected())
        return self_el
    
class Slider(Widget):
    def __init__(self, value=0, min=0, max=100,  name=None, on_change=None, **kwargs):
        self.value = value
        self.min = min
        self.max = max
        self.on_change = on_change
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        var_to_bind = tk.DoubleVar(value=self.value)
        if isinstance(self.value, ViewModelBindable):
            var_to_bind.set(self.value.get_value())
            self.value.connect_tk_var(var_to_bind)
            self.value = self.value.get_value()
        return var_to_bind

    def layout_tk_widget(self, parent):
        widget = ttk.Scale(parent.el, from_=self.min, to=self.max, variable=self.var_to_bind, **self.styles)
        if self.on_change is not None:
            widget.bind('<ButtonRelease-1>', lambda val:self.on_change())
        return widget

class NumericUpDown(Widget):
    def __init__(self, value=None, min=0, max=100, name=None, on_change=None, **kwargs):
        self.value = value
        self.min = min
        self.max = max
        self.on_change = on_change
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        var_to_bind = tk.IntVar()
        if isinstance(self.value, ViewModelBindable):
            var_to_bind.set(self.value.get_value())
            self.value.connect_tk_var(var_to_bind)
            self.value = self.value.get_value()
        else:
            var_to_bind.set(self.value)
        return var_to_bind

    def layout_tk_widget(self, parent):
        return ttk.Spinbox(parent.el, from_=self.min, to=self.max, textvariable=self.var_to_bind, command=self.on_change, **self.styles)
    
class ProgressBar(Widget):
    def __init__(self, value=None, name=None, **kwargs):
        self.value = value
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        if isinstance(self.value, ViewModelBindable):
            self.value.on_change(lambda v: self.set_value(v))
            self.value = self.value.get_value()
        return None

    def get_value(self):
        return self.el['value']
    
    def set_value(self, value):
        self.el['value'] = value

    def layout_tk_widget(self, parent):
        el = ttk.Progressbar(parent.el, **self.styles)
        el['value'] = self.value
        return el
    
class GroupBox(Widget):
    def __init__(self, text='Frame', children=[], name=None, **kwargs):
        self.children = children
        self.text = text
        super().__init__(name=name, **kwargs)

    def layout_tk_widget(self, parent):
        self.el = ttk.LabelFrame(parent.el, text=self.text, **self.styles)
        self.column = Column(self.children, **self.styles).build(self)
        self.el.columnconfigure(0, weight=1)
        self.el.rowconfigure(0, weight=1)
        self.column.grid(row=0, column=0, sticky="wens")
        return self.el
    
class TabControl(Widget):
    def __init__(self, tabs={'Tab': []}, name=None, **kwargs):
        self.tabs = tabs
        super().__init__(name=name, **kwargs)

    def layout_tk_widget(self, parent):
        self.el = ttk.Notebook(parent.el, **self.styles)
        for label, children in self.tabs.items():
            frame_el = Column(children).build(self)
            frame_el.pack(fill='both', expand=True)
            self.el.add(frame_el, text=label)
        return self.el
    
class FilePicker(Widget):
    def __init__(self, text="Select File...", value='', filetypes=[('All files', '*.*')], multiple=False, dir=False, name=None, **kwargs):
        self.text = text
        self.filetypes = filetypes
        self.multiple = multiple
        self.dir = dir
        self.value = value
        super().__init__(name=name, **kwargs)

    def get_value(self):
        if isinstance(self.value, ViewModelBindable):
            return self.value.get_value()
        else:
            return self.value
    
    def set_value(self, value):
        if isinstance(self.value, ViewModelBindable):
            self.value.set_value(value)
        self.label.el['text'] = value

    def on_pick_file(self):
        value = None
        if self.dir:
            value = filedialog.askdirectory(title=self.text)
        elif self.multiple:
            value = filedialog.askopenfilenames(title=self.text, filetypes=self.filetypes)
        else:
            value = filedialog.askopenfilename(title=self.text, filetypes=self.filetypes)
        self.label.el['text'] = self.value
        if isinstance(self.value, ViewModelBindable):
            self.value.set_value(value)

    def layout_tk_widget(self, parent):
        self.button = Button(self.text, on_click=self.on_pick_file)
        self.label = Label(self.value, width=30)
        return Row([self.button, self.label], **self.styles).build(parent)
    
class Canvas(Widget):
    def layout_tk_widget(self, parent):
        return tk.Canvas(parent.el, **self.styles)
    
class PictureBox(Widget):
    def __init__(self, image=None, name=None, **kwargs):
        self.image = image
        super().__init__(name=name, **kwargs)

    def get_value(self):
        raise RuntimeError('PictureBox only supports set_value')
    
    def set_value(self, value):
        self.el['image'] = value

    def layout_tk_widget(self, parent):
        return ttk.Label(parent.el, image=self.image, **self.styles)
    
class ShowIf(WrapperWidget):
    def __init__(self, condition_bindable:ViewModelBindable, children:list[Widget]=[], **kwargs):
        if not isinstance(condition_bindable, ViewModelBindable):
            raise RuntimeError('condition in ShowIf must be ViewModelBindable like "should_show_"')
        self.condition_bindable = condition_bindable
        condition_bindable.on_change(lambda v: self.update())
        super().__init__(children, **kwargs)

    def update(self):
        if self.condition_bindable.get_value():
            for child in self.children:
                child.el.grid()
        else:
            for child in self.children:
                child.el.grid_remove()

    def post_container_build(self):
        self.update()

    def layout_tk_widget(self, parent):
        self.update()
        return None
    
    
class DataTable(Widget):
    def __init__(
        self,
        header: List[str]=None,
        table_data: List[List[Any]]=None,
        name=None,
        data_frame = None,
        selected_item: Optional[Any | ViewModelBindable] = None,
        selected_index: Optional[int | ViewModelBindable] = None,
        **kwargs
    ):
        if data_frame is not None:
            if isinstance(data_frame, ViewModelBindable):
                data_frame.on_change(self._update_from_data_frame)
                df = data_frame.get_value()
            else:
                df = data_frame
            self.header = df.columns.tolist()
            self.table_data = df.values.tolist()
        else:
            self.header = header
            self.table_data = table_data

        self._selected_item = selected_item
        self._selected_index = selected_index
        super().__init__(name=name, **kwargs)

        # Check if table_data is bindable
        if isinstance(self.table_data, ViewModelBindable):
            self.table_data.on_change(self._handle_table_data_change)
            self.table_data = self.table_data.get_value()

        # Check if header is bindable
        if isinstance(self.header, ViewModelBindable):
            self.header.on_change(self._update_header)
            self.header = self.header.get_value()

        # Check if selected_item is bindable
        if isinstance(self._selected_item, ViewModelBindable):
            self._selected_item.on_change(self._update_selected_item_from_bindable)

        # Check if selected_index is bindable
        if isinstance(self._selected_index, ViewModelBindable):
            self._selected_index.on_change(self._update_selected_index_from_bindable)

    def _update_from_data_frame(self, new_df):
        """Update table when the bindable DataFrame changes."""
        self.header = new_df.columns.tolist()
        self.table_data = new_df.values.tolist()
        self._refresh_table()

    def _handle_table_data_change(self, new_data, change_type=None, data=None):
        """Handle different types of table data changes."""
        self.table_data = new_data
        if change_type is None:
            self._refresh_table()
        elif change_type == BindedListUpdateType.INSERT:
            self._insert_row(len(self.table_data) - 1, data)
        elif change_type == BindedListUpdateType.INSERT_AT:
            index, row = data
            self._insert_row(index, row)
        elif change_type == BindedListUpdateType.DELETE_ROW:
            self._delete_row(data)
            # Update selected index if the deleted row is before or is the selected row
            if isinstance(self._selected_index, int) and data <= self._selected_index:
                if isinstance(self._selected_index, ViewModelBindable):
                    self._selected_index.set_value(self._selected_index)
                else: 
                    self._selected_index -= 1
        elif change_type == BindedListUpdateType.SET_CELL:
            row_index, col_index, value = data
            self._set_cell(row_index, col_index, value)
        elif change_type == BindedListUpdateType.SETITEM:
            index, row = data
            self._update_row(index, row)

    def _update_selected_item_from_bindable(self, new_item):
        """Update the table selection based on the bindable selected item."""
        try:
            index = self.table_data.index(new_item)
            self._select_row(index)
            if isinstance(self._selected_index, ViewModelBindable):
                self._selected_index.set_value(index)
            else:
                self._selected_index = index
        except ValueError:
            pass

    def _update_selected_index_from_bindable(self, new_index):
        """Update the table selection based on the bindable selected index."""
        if 0 <= new_index < len(self.table_data):
            self._select_row(new_index)
            if isinstance(self._selected_item, ViewModelBindable):
                self._selected_item.set_value(self.table_data[new_index])
            else:
                self._selected_item = self.table_data[new_index]

    def _select_row(self, index):
        """Select a row in the table by index."""
        children = self.el.get_children()
        if index < len(children):
            self.el.selection_set(children[index])

    def _update_header(self, new_header):
        """Update header when the bindable header changes."""
        self.header = new_header
        self.el["columns"] = self.header
        for col in self.header:
            self.el.heading(col, text=col)

    def _insert_row(self, index, row):
        """Insert a new row at the specified index."""
        self.el.insert("", index, values=row)

    def _delete_row(self, index):
        """Delete a row at the specified index."""
        children = self.el.get_children()
        if index < len(children):
            self.el.delete(children[index])

    def _set_cell(self, row_index, col_index, value):
        """Set the value of a specific cell."""
        children = self.el.get_children()
        if row_index < len(children):
            item = children[row_index]
            values = list(self.el.item(item, "values"))
            values[col_index] = value
            self.el.item(item, values=values)

    def _update_row(self, index, row):
        """Update an existing row."""
        children = self.el.get_children()
        if index < len(children):
            self.el.item(children[index], values=row)

    def _refresh_table(self):
        """Refresh the entire table, including header and data."""
        # Clear existing data
        for item in self.el.get_children():
            self.el.delete(item)

        # Configure columns
        self.el["columns"] = self.header
        self.el["show"] = "headings"
        for col in self.header:
            self.el.heading(col, text=col)
            self.el.column(col, width=100)

        # Insert new data
        for row in self.table_data:
            self.el.insert("", tk.END, values=row)

    def layout_tk_widget(self, parent):
        self.el = ttk.Treeview(parent.el, **self.styles)
        self._refresh_table()
        self.el.bind('<<TreeviewSelect>>', self._on_select)
        return self.el

    def _on_select(self, event):
        """Handle the selection event of the table."""
        selected_items = self.el.selection()
        if selected_items:
            item = selected_items[0]
            children = self.el.get_children()
            index = children.index(item)
            if isinstance(self._selected_index, ViewModelBindable):
                self._selected_index.set_value(index)
            else:
                self._selected_index = index
            if isinstance(self._selected_item, ViewModelBindable):
                self._selected_item.set_value(self.table_data[index])
            else:
                self._selected_item = self.table_data[index]