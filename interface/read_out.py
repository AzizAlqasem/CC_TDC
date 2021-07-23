from interface import cci
from settings.settings import settings
from interface.data_tools import raw_data_to_channel_arr, channel_arr_to_count_ar


class ReadOut:

    def __init__(self):
        pass
    
    def init(self,):
        self.cc_usb = cci.CC_USB(
        commands=settings.generate_commands, time_out_ms=settings.get_setting("cc_time_out_ms"), 
        LAM=settings.get_setting("LAM"), 
        trig_delay_us=settings.get_setting("trig_delay_us"), 
        buffer_opt=settings.get_setting("buffer_opt")
        )
        self.target_modules = settings.get_setting("target_modules") #list
        self.module_list = []
        for target in target_modules:
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
    
    def get_number_of_data_chunck(self):
        self.number_of_data_chunck = self.raw_data[0]
    
    def get_channel_arr(self,):
        self.channel_data_arr = raw_data_to_channel_arr(self.raw_data)
    
    def _split_channel_arr_between_modules(self,):
        self.channel_data_dict {}
        s = 0
        for i, module in enumarate(self.target_modules):
            nodch_list = [settings.get_setting('nodch', target=module) for module in self.target_modules]
            e = nodch_list[i]
            ch_arr = self.channel_data_arr[:, s:e] #*
            mcv = settings.get_setting('min_count_value', target=module)
            mxcv = settings.get_setting('max_count_value', target=module)
            data_arr = channel_arr_to_count_ar(ch_arr, mcv, mxcv)
            self.channel_data_dict[module] = (ch_arr, data_arr)
    
    def get_data(self,): # Public
        self.get_raw_data()
        self.get_number_of_data_chunck()
        self.get_channel_arr()
        self._split_channel_arr_between_modules()
        return self.channel_data_dict, self.number_of_data_chunck


read_out = ReadOut()