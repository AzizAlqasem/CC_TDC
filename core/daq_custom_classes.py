from core.classes import DAQ, Threading
from settings.settings import settings
from interface.read_out import read_out
from settings.settings import settings
from time import sleep
import numpy as np


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

    def get_tot_avg_hit(self, last=None): # redendencies with DAQ
        tot_avg_hit_list = []
        for tdc in self.tdcs_obj_list:
            avg = tdc.get_tot_avg_hit(last=last)
            tot_avg_hit_list.append([tdc.name, avg])
        return tot_avg_hit_list

    def _run(self,):
        # get data fron TDC
        data = read_out.get_data()
        if data:
            channel_data_dict, number_of_data_chunck = data
            # update
            for tdc in self.tdcs_obj_list:
                ch_arr, data_arr, avg_hit = channel_data_dict[tdc.name]
                tdc.arr += data_arr
                # tdc.channel_arr = ch_arr
                tdc.avg_hit_list.append(avg_hit)
            self.tot_laser_shot += number_of_data_chunck

            if self.loop_counter % self.auto_save_delay == 0:
                for tdc in self.tdcs_obj_list:
                    tdc.auto_save()

            self.loop_counter += 1
            #print("R DAQ")
            sleep(0.5)

    def save(self, path, info):
        for tdc in self.tdcs_obj_list:
            info["Module name"] = tdc.name
            info["Time Resolution (ns)"] = tdc.time_resolution
            info["Average hit/shot"] = tdc.get_tot_avg_hit()
            info["Total Laser shot"] = self.tot_laser_shot
            tdc.save(path, info)


