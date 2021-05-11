from connection import Connection
from config import Config
from gui import gui

config = Config()
api_token = config.get_api_token()
url = config.get_url()

con = Connection(url, api_token)
gui(con,config)

