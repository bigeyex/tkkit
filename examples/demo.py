from tkkit import *


app = TKApp('My App')

def set_button_2():
    app.set_text('button_2', "changed")
    print(app.get_value('text2'))
    app.set_value('text2', 'changed')

def button_3_click():
    app.replace('col1', Column([Label('This have been changed')]))
    
def checkbox_click():
    print(app.get_value('check1'))

def radio_click():
    print(app.get_value('radio1'))

def combo_change():
    print(app.get_value('combo1'))

def listbox_change():
    print(app.get_value('listbox1'))

def select_list_button():
    app.set_value('listbox1', ('third', 'second'))

def slider_change():
    print(app.get_value('slider1'))

def numeric_change():
    app.set_value('progress1', app.get_value('numeric1'))

window = Window([
    Row([Button('One', on_click=set_button_2), Button('Two', name="button_2"), Button('Three', on_click=button_3_click)], align='center', bg='yellow'),
    Row([
        Column([Button('Select List', on_click=select_list_button), Label('Two'),
                ProgressBar(name='progress1', expand=1),
                NumericUpDown(name="numeric1", on_change=numeric_change),
                Slider(name="slider1", on_change=slider_change),
                ListBox(('first', 'second', 'third', '4th', '5th'), lines=3, name="listbox1", multiple=True, on_change=listbox_change),
                CheckBox('Checkbox One', name="check1", on_click=checkbox_click, checked=True, align="right"),
                ComboBox(values=('uno', 'dos', 'tres'), selected='tres', on_change=combo_change, name="combo1"),
                RadioButton('Radio 1', 'radio1', name="radio1", on_click=radio_click),
                RadioButton('Radio 2', name="radio1", on_click=radio_click, selected=True),
                RadioButton('Radio 3', name="radio1", on_click=radio_click),
                ], name='col1', align="left", expand=0, bg='red'),
        Column([TextBox('One', name="text1")], expand=1, vertical_align="top"),
        Column([TextBox('', lines=5, password=True, name='text2'), Button('Two'), Button('Three')], width=50, align="right"),
    ])
], bg='green')

app.show(window)
app.run()
