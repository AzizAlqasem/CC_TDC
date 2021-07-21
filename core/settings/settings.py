


class Settings:

    def __init__(self,):
        self._load_settings()

    def get_settings(self, setting:str):
        assert setting in self.settings_dict
        return self.settings_dict[setting]

    def update(self, key, value): #Fetch settings from Settings page in the app
        #Read app settings and save changes
        assert key in self.settings_dict
        self.settings_dict[key] = str(value)

    
    def _load_settings(self, path='Default_settings.txt'):
        with open(path, 'r') as sf:
            setting_text = sf.read().replace('\r','')
        self.settings_dict = {}
        for line in setting_text.split('\n'):
            if line.startswith("#") or ":" not in line: #This is valued for header only
                continue
            key, *value = line.split(":")
            value = ' '.join(value)
            self.settings_dict[key] = value


