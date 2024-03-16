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
