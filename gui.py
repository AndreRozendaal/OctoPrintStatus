import PySimpleGUI as sg

def gui(con):
    configfile = "test-octoprint.ini"
    menu_def = [
        ['Edit', ['Configuration'], ],
        ['view', ['Status Bar'], ],
        ['Help', ['About Octoprint'], ], ]
    WIN_W = 90
    WIN_H = 25
    interval = 5000

    layout = [[sg.Menu(menu_def)],
              [sg.Text('Temp bed:'), sg.Text(size=(WIN_W, 1), key="bed")],
              [sg.Text('Temp nozzle:'), sg.Text(size=(WIN_W, 1), key="nozzle")],

              [sg.Text(''), sg.Text(size=(WIN_W, 1), key="text2")],
              [sg.StatusBar(text=f'ok', size=(WIN_W, 1), pad=(0, 0), text_color='black',
                            background_color='white', relief=sg.RELIEF_FLAT, justification='left', visible=False,
                            key='status_bar')]
              ]
    status_bar_switch = True
    window = sg.Window(f"Octoprint", layout, keep_on_top=False, resizable=True, finalize=True)
    while True:
        result = con.get_all()
        window['bed'].update(result["temp_bed"])
        window['nozzle'].update(result["temp_nozzle"])
        event, values = window.read(timeout=interval)

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Status Bar':
            if status_bar_switch:
                window['status_bar'].ParentRowFrame.pack(fill='x')
                window['status_bar'].update(visible=True)
                window['status_bar'].Widget.pack(fill='x')
                status_bar_switch = False
            else:
                window['status_bar'].update(visible=False)
                window['status_bar'].ParentRowFrame.pack_forget()
                status_bar_switch = True
        if event == "Configuration":
            print("configuration")
        if event == "About Octoprint":
            print("about")
    window.close()
