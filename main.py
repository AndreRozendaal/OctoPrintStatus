from connection import Connection
from gui import gui

api_token = 'fake_api_key'
url = "http://192.168.2.55/api"

con = Connection(url, api_token)
gui(con)
