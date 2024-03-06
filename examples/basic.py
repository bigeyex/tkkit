from tkkit import TKApp, Button, Window, Row, Column


app = TKApp('My App')

def set_button_2():
    app.set('button_2', 'text', "changed")

window = Window([
    Row([Button('One', on_click=set_button_2), Button('Two', name="button_2"), Button('Three')]),
    Row([
        Column([Button('One'), Button('Two')]),
        Column([Button('One')]),
        Column([Button('One'), Button('Two'), Button('Three')]),
    ])
])

app.show(window)
app.run()
