import configparser

class Config:
    def __init__(self):
         self.filename = "OctoPrintStatus.ini"
         self.config = configparser.ConfigParser()
         if not self.configfile_exist():
             self.create_configfile()

    def configfile_exist(self):
        data = self.config.read(self.filename)
        return True if len(data) == 1 else False

    def create_configfile(self):
        self.config.has_section('settings')
        self.write_configfile()

    def write_configfile(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def set_url(self, url):
        if self.config.has_section('settings'):
            self.config['settings']['url'] = url
        else:
            self.config.add_section('settings')
            self.config['settings']['url'] = url
        self.write_configfile()

    def set_api_token(self, api_token):
        if self.config.has_section('settings'):
            self.config['settings']['api_token'] = api_token
        else:
            self.config.add_section('settings')
            self.config['settings']['api_token'] = api_token
        self.write_configfile()

    def get_url(self):
        self.config.read(self.filename)
        if self.config.has_section('settings'):
            return self.config['settings']['url']

    def get_api_token(self):
        self.config.read(self.filename)
        if self.config.has_section('settings'):
            return self.config['settings']['api_token']
