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

window = Window([
    Row([Button('One', on_click=set_button_2), Button('Two', name="button_2"), Button('Three', on_click=button_3_click)]),
    Row([
        Column([Button('One'), Label('Two'),
                CheckBox('Checkbox One', name="check1", on_click=checkbox_click, checked=True),
                ComboBox(values=('uno', 'dos', 'tres'), selected='tres', on_change=combo_change, name="combo1"),
                RadioButton('Radio 1', 'radio1', name="radio1", on_click=radio_click),
                RadioButton('Radio 2', name="radio1", on_click=radio_click, selected=True),
                RadioButton('Radio 3', name="radio1", on_click=radio_click,),
                ], name='col1'),
        Column([TextBox('One', name="text1")]),
        Column([TextBox('', lines=5, password=True, name='text2'), Button('Two'), Button('Three')]),
    ])
])

app.show(window)
app.run()
