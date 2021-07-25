
SUPPORTED_TARGETS = ["TDC2228A", "TDC4208"]
POST_CALCULATIONS = ["tot_nodch", "arr_size", 'start_marker']

class Settings:

    def __init__(self,):
        self._load_settings()

        self.post_calculations()

    def get_setting(self, setting:str, target=None):
        assert setting in self.settings_dict
        if target:
            assert target in SUPPORTED_TARGETS
            setting = target + "_" + setting
        return self.settings_dict[setting]

    def set_setting(self, key, value, target=None): #Fetch settings from Settings page in the app
        #Read app settings and save changes
        if target:
            assert target in SUPPORTED_TARGETS
            key = target + "_" + setting
        assert key in self.settings_dict
        self.settings_dict[key] = str(value)

        #* not efficient!
        self.post_calculations()

    def _load_settings(self, path='Default_settings.txt'):
        with open(path, 'r') as sf:
            setting_text = sf.read().replace('\r','')
        self.settings_dict = {}
        for line in setting_text.split('\n'):
            if line.startswith("#") or ":" not in line: #This is valued for header only
                continue
            line = line[ : line.find('#')].replace(' ', '')
            key, value = line.split("=")
            if value.startswith("[") or "," in value:
                value = value.replace("[",'').replace("]", '')
                value = value.split(",")
            self.settings_dict[key] = value
    
    def generate_commands(self):
        target_modules = self.get_setting("target_modules")
        commands = []
        if "TDC2228A" in target_modules:
            N = self.get_setting("TDC_2228A_slot_number")
            noch = self.get_setting("TDC_2228A_nodch")
            for A in range(noch):  # Read all channels
                commands.append([N, A, 0])
            commands.append([N, 0, 9]) #commands to clear Data

        if "TDC4208" in target_modules:
            N = self.get_setting("TDC_4208_slot_number")
            noch = self.get_setting("TDC_4208_nodch)
            for A in range(noch):  # Read all channels
                commands.append([N, A, 0])
            commands.append([N, 0, 9]) #commands to clear Data

        return commands

    def post_calculations(self,):
        # tot_nodch:
        self.targets = self.get_setting("target_modules")
        tot_nodch = sum(self.get_setting('nodch', target=target) for target in targets)
        self.settings_dict["tot_nodch"] = tot_nodch

        # Array size:
        for target in self.targets:
            minv = self.get_setting('min_count_value', target=target)
            maxv = self.get_setting('max_count_value', target=target)
            self.set_setting(key="arr_size", value=int(maxv)-int(minv), target=target)
        
        # Start Marker: define how many data point in each loop, taken from tdc(s)
        self.settings_dict["start_marker"] = tot_nodch + 1 # "1" is the size of end marker


 settings = Settings()
 