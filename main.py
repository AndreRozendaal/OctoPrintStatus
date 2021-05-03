from connection import Connection
from gui import gui

api_token = '799172DF4A5F4ACAA50BED5B3036B0C0'
url = "http://192.168.2.55/api"

con = Connection(url, api_token)
gui(con)
