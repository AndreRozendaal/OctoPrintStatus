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
            return json.loads(response)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def get_printer(self):
        return self.get("/printer")

    def get_job(self):
        return self.get("/job")

    def get_all(self):
        data = {
            "temp_bed": "N/A",
            "temp_nozzle": "N/A",
            "printer_status": "N/A",
            "elapsed_time": "N/A"
        }
        printer = self.get_printer()
        # job = self.get_job()
        # print(job)
        # printer = self.get("/printer")
        if printer.get("error"):
            data["printer_status"] = "Printer not operational"
        else:
            if printer.get("temperature"):
                temperature = printer["temperature"]
                if temperature.get("bed"):
                    data["temp_bed"] = printer["temperature"]["bed"]["actual"]
                if temperature.get("tool0"):
                    data["temp_nozzle"] = printer["temperature"]["tool0"]["actual"]
            if printer.get("state"):
                state = printer["state"]
                if state["flags"]["operational"] == "true" and state["flags"]["printing"] == "false":
                    data["printer_status"] = "Printer Operational"
                elif state["flags"]["operational"] == "true" and state["flags"]["printing"] == "true":
                    data["printer_status"] = "Printing"
                else:
                    data["printer_status"] = "Printer not operational"
        return data
