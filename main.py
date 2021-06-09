from connection import Connection
from config import Config
from gui import gui

# Read configuration file for api_token and url of OctoPrint
config = Config()
api_token = config.get_api_token()
url = config.get_url()

# Make connection to OctoPrint
con = Connection(url, api_token)

# Start Gui
gui(con, config)
