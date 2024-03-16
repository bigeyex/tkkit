# tkkit
Make Desktop Application with ease.

I used to write (Windows/Mac) desktop apps with tkinter at work, but found that although tkinter 
comes with pack and grid layouts, writing the ui part still takes a lot of time. 

Inspired by modern web development, tkkit(tkinter kit) is a simple tkinter wrapper that 
simplifies ui layouting and provides a consistent api. Its features include:

- depends only on tkinter, which comes with Python by default. 
- Simple Row and Column Layout.
- "HTML/React" markup style compoments
- event callbacks like `on_click` run on a separate thread

learn more at [Wiki/Documentation](https://github.com/bigeyex/tkkit/wiki/Quick-Start)

## Installation 

```python
pip install tkkit
```

## Example

```python
from tkkit import *

app = TKApp('My App')

def copy_text():
    app.set_text("label1", app.get_value("text_box"))

def get_label_value():
    app.set_text("label2", app.get_value("radios"))

window = Window([
    Row([Button('Get Text', on_click=copy_text), 
         Button('Get Radio Value', on_click=get_label_value)]),
    Row([
        Column([TextBox("", name="text_box"), Label('Press Button', name="label1")]),
        Column([
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
- [] Bind, Events
- [] Dataframe, TreeView