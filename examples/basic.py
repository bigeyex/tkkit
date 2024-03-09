from tkkit import TKApp, Button, Window, Row, Column, Label


app = TKApp('My App')

def set_button_2():
    app.set_text('button_2', "changed")

window = Window([
    Row([Button('One', on_click=set_button_2), Button('Two', name="button_2"), Button('Three')]),
    Row([
        Column([Button('One'), Label('Two')]),
        Column([Button('One')]),
        Column([Button('One'), Button('Two'), Button('Three')]),
    ])
])

app.show(window)
app.run()
