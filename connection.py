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

    def get_all(self):
        return self.get("/printer")
