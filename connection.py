import requests
import json
import random


class Connection:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': api_key}

        self.reset_data()
        self.demo_mode = False
        self.demo_phase = 0

    def update_url(self, url):
        self.url = url

    def update_api_token(self,api_key):
        self.api_key = api_key

    def __str__(self):
        return f"url: {self.url}\napi_key: {self.api_key}"

    def get(self, api_call):
        try:
            response = requests.get(self.url + api_call, headers=self.headers).text
        except requests.exceptions.ConnectionError as e:
            value = {"error": str(e)}
            return True, json.dumps(value)
        except requests.exceptions.RequestException as e:
            # raise SystemExit(e)
            value = {"error": str(e)}
            return True, json.dumps(value)
        except:
            value = {"error": "Connection error"}
            return True, json.dumps(value)
        return False, json.loads(response)

    def get_printer(self):
        if self.demo_mode:
            self.demo_phase = self.demo_phase + 1
            if self.demo_phase > 20: self.demo_phase = 0
            return False, {"sd": {"ready": "false"}, "state": {"error": "", "flags":
                {"cancelling": "false", "closedOrError": "false", "error": "false", "finishing": "false",
                 "operational": "true",
                 "paused": "false", "pausing": "false", "printing": "false", "ready": "true", "resuming": "false",
                 "sdReady": "false"},
                                                        "text": "Operational"},
                    "temperature": {"bed": {"actual": self.demo_phase + 60 + random.randint(0,3),  "offset": 0, "target": 0.0},
                                    "tool0": {"actual": self.demo_phase + 180 + random.randint(0,20), "offset": 0, "target": 0.0}}}

        else:
            return self.get("/printer")

    def get_job(self):
        if self.demo_mode:
            return (False,{'error': '', 'job': {'averagePrintTime': None, 'estimatedPrintTime': None, 'filament': None, 'file': {'date': None, 'display': None, 'name': None, 'origin': None, 'path': None, 'size': None}, 'lastPrintTime': None, 'user': None}, 'progress': {'completion': 10.5555, 'filepos': None, 'printTime': None, 'printTimeLeft': 300, 'printTimeLeftOrigin': None}, 'state': 'Printing'})
        else:
            return self.get("/job")

    def reset_data(self):
        self.data = {
            "temp_bed": "N/A",
            "temp_nozzle": "N/A",
            "printer_status": " ",
            "printTimeLeft": "N/A",
            "completion": "N/A"
        }

    def get_all(self):
        self.reset_data()
        error, printer = self.get_printer()
        job = self.get_job()

        if error:
            self.data["printer_status"] = "Connection Error"
        else:
            if printer.get("temperature"):
                temperature = printer["temperature"]
                if temperature.get("bed"):
                    if isinstance(printer["temperature"]["bed"]["actual"], float):  self.data["temp_bed"]= round(printer["temperature"]["bed"]["actual"], 1)
                    else:
                        self.data["temp_bed"] = printer["temperature"]["bed"]["actual"]
                if temperature.get("tool0"):
                    if isinstance(printer["temperature"]["tool0"]["actual"], float):  self.data["temp_nozzle"] = round(
                        printer["temperature"]["tool0"]["actual"], 1)
                    else:
                        self. data["temp_nozzle"] = printer["temperature"]["tool0"]["actual"]
                self.data["printer_status"] = "Printer not operational"

            if job[1].get("progress"):
                if isinstance(job[1]["progress"]["completion"], float):
                    self.data["completion"] = str(round(job[1]["progress"]["completion"],1)) + "%"
                else:
                    self.data["completion"] = "N/A"
                if isinstance(job[1]["progress"]["printTimeLeft"], int):
                    self.data["printTimeLeft"] = str(round(job[1]["progress"]["printTimeLeft"]/60)) + " min"
                else:
                    self.data["printTimeLeft"] = "N/A"
                self.data["printer_status"] = job[1]["state"]

        return self.data

