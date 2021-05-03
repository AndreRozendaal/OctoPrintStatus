import PySimpleGUI as sg

def gui(con):
    configfile = "test-octoprint.ini"
    menu_def = [
        ['Edit', ['Configuration'], ],
        ['view', ['Status Bar'], ],
        ['Help', ['About Octoprint'], ], ]
    WIN_W = 50
    WIN_H = 25
    interval = 5000

    col_bed = [
        [sg.T('N/A', key="bed", size=(5,1), tooltip="Bed temperature")],
    ]

    col_nozzle = [
        [sg.T('N/A', key="nozzle", size=(5,1), tooltip="Nozzle temperature")],
    ]

    col_completion = [
        [sg.T('N/A', key="completion", size=(5,1), tooltip="Complete percentage")],
    ]

    col_remaining = [
        [sg.T('N/A', key="printTimeLeft", size=(5,1), tooltip="Remaining time")],
    ]
    layout = [[sg.Menu(menu_def)],
            [sg.Frame('', col_nozzle),
               sg.Frame('', col_bed)],
              [sg.Frame('', col_completion),
               sg.Frame('', col_remaining)],
              [sg.StatusBar(text=f'', pad=(5, 5), size=(100,1),  text_color='black',
                            background_color='white', relief=sg.RELIEF_FLAT, justification='left', visible=True,
                            key='status_bar')]]

    status_bar_switch = False
    window = sg.Window(f"Octoprint", layout, keep_on_top=False, resizable=True, finalize=True, size=(162,110))
    while True:
        result = con.get_all()

        window['bed'].update(result["temp_bed"])
        window['nozzle'].update(result["temp_nozzle"])
        window['printTimeLeft'].update(result["printTimeLeft"])
        window['completion'].update(result["completion"])
        window['status_bar'].update(result["printer_status"])

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
            print("must implement configuration window")
        if event == "must implement About Octoprint window":
            print("about")
    window.close()
