# tkkit
Make Desktop Application with ease.

I used to write (Windows/Mac) desktop apps with tkinter at work, but found that although tkinter 
comes with pack and grid layouts, writing the ui part still takes a lot of time. 

Inspired by modern web development and SwiftUI, tkkit(tkinter kit) is a simple tkinter wrapper that 
simplifies ui layouting and provides a consistent api. Its features include:

- depends only on tkinter, which comes with Python by default. 
- Simple VStack, HStack Layout.
- "HTML/React" markup style compoments
- event callbacks like `on_click` run on a separate thread
- Data binding with ViewModels
- DataTable supports plain array or pandas dataframe

learn more at [Wiki/Documentation](https://github.com/bigeyex/tkkit/wiki)

## Installation 

```python
pip install tkkit
```

## Example

### Hello World
```python
from tkkit import *

app = TKApp('My App')
window = VStack([
    Label('Hello World'),
])

app.show(window)
app.run()

```

### Use Bindings

create a `ViewModel` and use syntax with trailing `_` to bind attributes to ui elements.

```python
from tkkit import *

app = TKApp('My App')
vm = ViewModel()
vm.text = "Hello"

def on_button_click():
    vm.text = "World"

window = VStack([
    Label(vm.text_),
    TextBox(vm.text_),
    Button('Click Me', on_click=on_button_click),
])
```

### Use ShowIf to conditionally show or hide elements

```python
from tkkit import *

app = TKApp('My App')
vm = ViewModel()

window = VStack([
    CheckBox("Check Me", checked=vm.checked_),
    ShowIf(vm.checked_, [
        Label("Checkbox is checked!!"),
        Label("Checkbox is checked!!!"),
    ]),
])

app.show(window)
app.run() 
```

### Use DataTable

see [Example with plain array](examples/datatable.py) and [Example with pandas dataframe](examples/datatable_df.py)


### Set and Get Values Directly

While not recommended, you can also set and get values directly with `app.set_value` and `app.get_value`.

```python
from tkkit import *

app = TKApp('My App')

def copy_text():
    app.set_text("label1", app.get_value("text_box"))

def get_label_value():
    app.set_text("label2", app.get_value("radios"))

window = VStack([
    HStack([Button('Get Text', on_click=copy_text), 
         Button('Get Radio Value', on_click=get_label_value)]),
    VStack([
        HStack([TextBox("", name="text_box"), Label('Press Button', name="label1")]),
        HStack([
            Label('Radio Value', name="label2"),
            RadioButton('Radio 1', 'radio1', name="radios"),
            RadioButton('Radio 2', name="radios"),
            RadioButton('Radio 3', name="radios"),
        ]),
    ])
])

app.show(window)
app.run()
 
```


# TODO
- [] Dataframe, TreeView
- [] ShowFor