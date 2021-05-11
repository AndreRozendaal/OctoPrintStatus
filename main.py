from connection import Connection
from config import Config
from gui import gui

# api_token to my OctoPrint test instance
#api_token = '799172DF4A5F4ACAA50BED5B3036B0C0'
#url = "http://192.168.2.55/api"

config = Config()
api_token = config.get_api_token()
url = config.get_url()

con = Connection(url, api_token)
gui(con,config)

