import PySimpleGUI as sg


def configuration_windows(url, apikey):
    layout = [
        [sg.Text("Url:")],
        [sg.InputText(key="url")],
        [sg.Text("Api key:")],
        [sg.InputText(key="apikey")],
        [sg.Submit(), sg.Cancel()],
    ]

    window = sg.Window("Configuration Window", layout, modal=True, finalize=True)
    window["url"].update(url)
    window["apikey"].update(apikey)
    while True:
        event, values = window.read()
        if event in ("Cancel", sg.WIN_CLOSED):
            window.close()
            return False

        if event == "Submit":
            window.close()
            return {"url": values["url"], "api_token": values["apikey"]}


def gui(con, config):
    menu_def = [
        [
            "Edit",
            ["Configuration"],
        ],
        [
            "view",
            ["Status Bar", "Demo Mode"],
        ],
    ]
    WIN_W = 50
    WIN_H = 25
    interval = 5000

    col_bed = [
        [sg.T("N/A", key="bed", size=(5, 1), tooltip="Bed temperature")],
    ]

    col_nozzle = [
        [sg.T("N/A", key="nozzle", size=(5, 1), tooltip="Nozzle temperature")],
    ]

    col_completion = [
        [sg.T("N/A", key="completion", size=(5, 1), tooltip="Complete percentage")],
    ]

    col_remaining = [
        [sg.T("N/A", key="printTimeLeft", size=(5, 1), tooltip="Remaining time")],
    ]
    layout = [
        [sg.Menu(menu_def)],
        [sg.Frame("", col_nozzle), sg.Frame("", col_bed)],
        [sg.Frame("", col_completion), sg.Frame("", col_remaining)],
        [
            sg.StatusBar(
                text=f"",
                pad=(5, 5),
                size=(100, 1),
                text_color="black",
                background_color="white",
                relief=sg.RELIEF_FLAT,
                justification="left",
                visible=True,
                key="status_bar",
            )
        ],
    ]

    status_bar_switch = False
    window = sg.Window(
        f"Octoprint",
        layout,
        keep_on_top=False,
        resizable=True,
        finalize=True,
        size=(162, 110),
    )
    while True:
        con.get_all()

        window["bed"].update(con.get_temp_bed())
        window["nozzle"].update(con.get_temp_nozzle())
        window["printTimeLeft"].update(con.get_time_left())
        window["completion"].update(con.get_completion())
        window["status_bar"].update(con.get_status())

        event, _ = window.read(timeout=interval)

        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Status Bar":
            if status_bar_switch:
                window["status_bar"].ParentRowFrame.pack(fill="x")
                window["status_bar"].update(visible=True)
                window["status_bar"].Widget.pack(fill="x")
                status_bar_switch = False
            else:
                window["status_bar"].update(visible=False)
                window["status_bar"].ParentRowFrame.pack_forget()
                status_bar_switch = True
        if event == "Demo Mode":
            if con.demo_mode:
                con.demo_mode = False
            else:
                con.demo_mode = True

        if event == "Configuration":
            api_token = config.get_api_token()
            url = config.get_url()
            config_window = configuration_windows(url, api_token)
            if config_window:
                con.update_url(config_window["url"])
                con.update_api_token(config_window["api_token"])
                config.set_url(config_window["url"])
                config.set_api_token(config_window["api_token"])
    window.close()
