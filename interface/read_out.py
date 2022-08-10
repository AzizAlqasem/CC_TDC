from settings.settings import settings
from interface.data_tools import raw_data_to_channel_arr, channel_arr_to_count_ar
import numpy as np
from interface import cci

class ReadOut:

    def __init__(self):
        pass

    def init(self,):
        self.cc_usb = cci.CC_USB(
        commands=settings.generate_commands(), time_out_ms=settings.get_setting("cc_time_out_ms"),
        LAM=settings.get_setting("LAM"),
        trig_delay_us=settings.get_setting("trig_delay_us"),
        buffer_opt=settings.get_setting("buffer_opt")
        )
        self.target_modules = settings.get_setting("target_modules") #list
        self.module_list = []
        for target in self.target_modules:
            module = cci.CC_Module(
                module_slot_number=settings.get_setting("slot_number", target=target)
                )
            self.cc_usb.connect_to_module(module)
            self.module_list.append(module)

    def connect(self):
        self.cc_usb.stack_write()
        self.cc_usb.write_LAM_mask()
        self.cc_usb.set_trigger_delay()
        for module in self.module_list: module.disable_LAM()
        self.cc_usb.set_buffer_size()
        for module in self.module_list: module.clear_LAM()
        self.cc_usb.set_data_aq_mode(ON=True)

    def close(self):
        self.cc_usb.close()

    def get_raw_data(self,):
        self.raw_data = self.cc_usb.bulk_read()
        if not self.raw_data:
            self.raw_data = None
        #print(self.raw_data)

    def get_number_of_data_chunck(self):
        self.number_of_data_chunck = self.raw_data[0]

    def get_channel_arr(self,):
        self.channel_data_arr = raw_data_to_channel_arr(self.raw_data)

    def _split_channel_arr_between_modules(self,):
        self.channel_data_dict = {}
        s = 0
        for i, module in enumerate(self.target_modules):
            nodch = settings.get_setting('nodch', target=module)
            e = s + nodch
            ch_arr = self.channel_data_arr[:, s:e] #*
            # print(np.average(ch_arr[:,0])) #* For debuging
            mcv = settings.get_setting('min_count_value', target=module)
            mxcv = settings.get_setting('max_count_value', target=module)
            data_arr, row_data_arr_size = channel_arr_to_count_ar(ch_arr, mcv, mxcv)
            self.channel_data_dict[module] = (ch_arr, data_arr, row_data_arr_size/self.number_of_data_chunck)  #avg hit = row_data_arr_size/self.number_of_data_chunck
            s = e

    def get_data(self,): # Public
        self.get_raw_data()
        if self.raw_data is None:
            return None
        self.get_number_of_data_chunck()
        self.get_channel_arr()
        self._split_channel_arr_between_modules()
        return self.channel_data_dict, self.number_of_data_chunck



class Random_data_test(ReadOut):
    def __init__(self, nom=1):
        self.nom = nom #number of modules
        self.target_modules = settings.get_setting("target_modules")

    def init(self,):
        pass # overwirte
    def connect(self,):
        pass
    def close(self,):
        pass

    def get_raw_data(self,):
        sm = settings.get_setting("start_marker")
        em = settings.get_setting("end_marker")
        cs = self.nom*8 + 2
        self.raw_data = np.random.randint(0, 2000, (409 * cs) + 2) # 2 is for the extra [409 and -1]
        self.raw_data[0] = 409
        self.raw_data[1:][::cs] = sm
        self.raw_data[1:][sm::cs] = -1
        self.raw_data[-1] = int(em)



read_out = ReadOut()
#read_out = Random_data_test(2)