import requests
import json


class Connection:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': api_key
        }

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
        return self.get("/printer")

    def get_job(self):
        return self.get("/job")

    def get_all(self):
        data = {
            "temp_bed": "N/A",
            "temp_nozzle": "N/A",
            "printer_status": "N/A",
            "printTimeLeft": "N/A",
            "completion": "N/A"
        }

        error, printer = self.get_printer()
        job = self.get_job()

        # printer = self.get("/printer")
        # if printer.get("error"):

        if error:
            data["printer_status"] = "Connection Error"
        else:
            if printer.get("temperature"):
                temperature = printer["temperature"]
                if temperature.get("bed"):
                    if isinstance(printer["temperature"]["bed"]["actual"], float):  data["temp_bed"]= round(printer["temperature"]["bed"]["actual"], 1)
                    else:
                        data["temp_bed"] = printer["temperature"]["bed"]["actual"]
                if temperature.get("tool0"):
                    if isinstance(printer["temperature"]["tool0"]["actual"], float):  data["temp_nozzle"] = round(
                        printer["temperature"]["tool0"]["actual"], 1)
                    else:
                        data["temp_nozzle"] = printer["temperature"]["tool0"]["actual"]
                data["printer_status"] = "Printer not operational"

            if job[1].get("progress"):
                if isinstance(job[1]["progress"]["completion"], float):
                    data["completion"] = str(round(job[1]["progress"]["completion"],1)) + "%"
                else:
                    data["completion"] = "N/A"
                if isinstance(job[1]["progress"]["printTimeLeft"], int):
                    data["printTimeLeft"] = str(round(job[1]["progress"]["printTimeLeft"]/60)) + " min"
                else:
                    data["printTimeLeft"] = "N/A"
                data["printer_status"] = job[1]["state"]

        return data

