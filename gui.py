import PySimpleGUI as sg

def configuration_windows(url,apikey):
    return_dict={}
    layout = [[sg.Text("Url:")],
              [sg.InputText(key='url')],
              [sg.Text("Api key:")],
              [sg.InputText(key='apikey')],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window("Configuration Window", layout, modal=True, finalize=True)
    window['url'].update(url)
    window['apikey'].update(apikey)
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            return False
            break
        if event == "Submit":
            window.close()
            return {"url": values['url'], "api_token": values['apikey']}
            break

def gui(con,config):
    menu_def = [
        ['Edit', ['Configuration'], ],
        ['view', ['Status Bar', 'Demo Mode'], ]]
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
        if event == 'Demo Mode':
            if con.demo_mode:
                con.demo_mode = False
            else:
                con.demo_mode = True

        if event == "Configuration":
            api_token = config.get_api_token()
            url = config.get_url()
            r = configuration_windows(url, api_token)
            if r:
                con.update_url(r['url'])
                con.update_api_token(r['api_token'])
                config.set_url(r['url'])
                config.set_api_token(r['api_token'])


    window.close()


#config.set_url(values['url'])
#config.set_api_token(values['apikey'])