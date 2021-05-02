from connection import Connection

api_token = 'fake_api_key'
url = "http://192.168.2.55/api"

con = Connection(url, api_token)
print(con)

dict_all = con.get_all()
print(dict_all)
