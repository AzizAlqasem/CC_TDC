from core.classes import DAQ, Threading
from settings.settings import settings
from interface.read_out import read_out
from settings.settings import settings
from time import sleep


class DCounter(Threading): 
    def __init__(self):
        self.init()

    def init(self,):
        self.auto_save_delay = settings.get_setting("auto_save_delay")
        # How many CC Modules do we have?:
        # Give each TDC module a DAQ obj
        tdcs = settings.get_setting("target_modules")
        self.tdcs_obj_list = []
        for tdc in tdcs:
            tdc_obj = DAQ(name = tdc)
            self.tdcs_obj_list.append(tdc_obj)
        self.clear()

    def clear(self):
        for tdc in self.tdcs_obj_list:
            #tdc.set_arr()
            tdc.init() # NOT self.init()
        
        self.tot_laser_shot = 0
        self.loop_counter = 0

    def get_tot_avg_hit(self):
        if self.avg_hit_list:
            return np.average(self.avg_hit_list)
        return np.nan
        
    def _run(self,):
        # get data fron TDC
        channel_data_dict, number_of_data_chunck = read_out.get_data()
        # update
        for tdc in self.tdcs_obj_list:
            ch_arr, data_arr = channel_data_dict[tdc.name]
            tdc.arr += data_arr
            tdc.channel_arr = ch_arr 
            tdc.avg_hit_list.append(data_arr.size/number_of_data_chunck)
        self.tot_laser_shot += number_of_data_chunck
        
        if self.loop_counter % self.auto_save_delay == 0:
            for tdc in self.tdcs_obj_list:
                tdc.auto_save()
        
        self.loop_counter += 1
        print("R DAQ")
        sleep(0.9)

