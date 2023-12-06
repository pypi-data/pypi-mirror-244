import PySimpleGUI as sg

sg.theme('DarkPurple')
layout = [
    [sg.Text("Hello world!")],
    [sg.Text("input a value:"), sg.InputText(key="a", enable_events=True)],
    [sg.Text("input b value:"), sg.InputText(key="b", enable_events=True)],
    [sg.Text("Result: "), sg.Text("", key="result")],
    [sg.Image(key="img")],
    [sg.Button("Ok"), sg.Button("Cancel")]
]

window = sg.Window("SDA Window", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event == "Ok":
        a = float(values['a'])
        b = float(values['b'])
        result = a+b
        window['result'].update(result)
        # window["img"].update("C:\\Users\\Gokuruto\\Pictures\\EXyFsNXU4AQj_f2.jpg")

window.close()