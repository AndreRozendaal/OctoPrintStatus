import requests
import json
import random


class Connection:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

        self.headers = {"Content-Type": "application/json", "X-Api-Key": api_key}

        # Variables for storing printer data
        self.temp_bed = "N/A"
        self.temp_nozzle = "N/A"
        self.status = "N/A"
        self.timeleft = "N/A"
        self.completion = "N/A"

        self.connection_error = True

        self.demo_mode = False
        self.demo_phase = 0

    def update_url(self, url):
        self.url = url

    def update_api_token(self, api_key):
        self.api_key = api_key

    def __str__(self):
        return f"url: {self.url}\napi_key: {self.api_key}"

    def get(self, api_call):
        try:
            response = requests.get(self.url + api_call, headers=self.headers).text

            if not response:
                self.status = "Http Error"
        except requests.exceptions.ConnectionError as error:
            value = {"error": str(error)}
            self.status = error
            return json.dumps(value)
        except requests.exceptions.RequestException as error:
            # raise SystemExit(e)
            value = {"error": str(error)}
            self.status = error
            return json.dumps(value)
        except requests.exceptions.HTTPError as error:
            value = {"error": str(error)}
            self.status = error
            return json.dumps(value)
        except:
            self.status = "Connection error"
            self.connection_error = True
            return json.dumps(value)
        self.connection_error = False
        return json.loads(response)

    def get_printer(self):
        if self.demo_mode:
            self.demo_phase = self.demo_phase + 1
            if self.demo_phase > 20:
                self.demo_phase = 0
            return {
                "sd": {"ready": "false"},
                "state": {
                    "error": "",
                    "flags": {
                        "cancelling": "false",
                        "closedOrError": "false",
                        "error": "false",
                        "finishing": "false",
                        "operational": "true",
                        "paused": "false",
                        "pausing": "false",
                        "printing": "false",
                        "ready": "true",
                        "resuming": "false",
                        "sdReady": "false",
                    },
                    "text": "Operational",
                },
                "temperature": {
                    "bed": {
                        "actual": self.demo_phase + 60 + random.randint(0, 3),
                        "offset": 0,
                        "target": 0.0,
                    },
                    "tool0": {
                        "actual": self.demo_phase + 180 + random.randint(0, 20),
                        "offset": 0,
                        "target": 0.0,
                    },
                },
            }

        else:
            return self.get("/printer")

    def get_job(self):
        if self.demo_mode:
            return {
                "error": "",
                "job": {
                    "averagePrintTime": None,
                    "estimatedPrintTime": None,
                    "filament": None,
                    "file": {
                        "date": None,
                        "display": None,
                        "name": None,
                        "origin": None,
                        "path": None,
                        "size": None,
                    },
                    "lastPrintTime": None,
                    "user": None,
                },
                "progress": {
                    "completion": 10.5555,
                    "filepos": None,
                    "printTime": None,
                    "printTimeLeft": 300,
                    "printTimeLeftOrigin": None,
                },
                "state": "Printing",
            }
        else:
            return self.get("/job")

    def reset_data(self):
        self.temp_bed = "N/A"
        self.temp_nozzle = "N/A"
        self.status = "N/A"
        self.timeleft = "N/A"
        self.completion = "N/A"

    def get_all(self):
        self.reset_data()
        try:
            printer = self.get_printer()
            job = self.get_job()
            print(printer)
            print(job)
            if self.connection_error:
                self.status = "Connection Error"
            else:
                if printer.get("temperature"):
                    temperature = printer["temperature"]
                    if temperature.get("bed"):
                        if isinstance(printer["temperature"]["bed"]["actual"], float):
                            self.temp_bed = round(
                                printer["temperature"]["bed"]["actual"], 1
                            )
                            print(self.temp_bed)
                        else:
                            self.temp_bed = printer["temperature"]["bed"]["actual"]
                            print(self.temp_bed)
                    if temperature.get("tool0"):
                        if isinstance(printer["temperature"]["tool0"]["actual"], float):
                            self.temp_nozzle = round(
                                printer["temperature"]["tool0"]["actual"], 1
                            )
                        else:
                            self.temp_nozzle = printer["temperature"]["tool0"]["actual"]
                    self.status = "Printer not operational"

                if job.get("progress"):
                    if isinstance(job["progress"]["completion"], float):
                        self.completion = (
                            str(round(job["progress"]["completion"], 1)) + "%"
                        )
                    else:
                        self.completion = "N/A"
                    if isinstance(job["progress"]["printTimeLeft"], int):
                        self.timeleft = (
                            str(round(job["progress"]["printTimeLeft"] / 60)) + " min"
                        )
                    else:
                        self.timeleft = "N/A"
                    self.status = job["state"]
        except Exception:
            pass

    def get_status(self):
        return self.status

    def get_temp_bed(self):
        return self.temp_bed

    def get_temp_nozzle(self):
        return self.temp_nozzle

    def get_time_left(self):
        return self.timeleft

    def get_completion(self):
        return self.completion

    def set_status(self, status):
        self.status = status
