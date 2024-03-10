from tkkit import *


app = TKApp('My App')

def set_button_2():
    app.set_text('button_2', "changed")
    print(app.get_value('text2'))
    app.set_value('text1', 'changed')

def button_3_click():
    app.replace('col1', Column([Label('This have been changed')]))

window = Window([
    Row([Button('One', on_click=set_button_2), Button('Two', name="button_2"), Button('Three', on_click=button_3_click)]),
    Row([
        Column([Button('One'), Label('Two')],  name='col1'),
        Column([TextBox('One', name="text1")]),
        Column([TextBox('', lines=5, password=True, name='text2'), Button('Two'), Button('Three')]),
    ])
])

app.show(window)
app.run()
