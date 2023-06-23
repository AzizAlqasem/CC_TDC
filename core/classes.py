import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import numpy as np
from threading import Thread
from settings.settings import settings
from streamlit.report_thread import add_report_ctx
import datetime


# General (Level 0) Class
#class Container:

#    def set_arr(self): #Also Clear
#        self.arr = np.zeros(self.size, dtype=self.type)


class Threading:

    def __init__(self):
        self.terminate = False # Terminate running Thread

        #Check the status of run loop
        self.is_running = False

    def run(self,):
        self.is_running = True
        while self.terminate==False:
            self._run()  # Having the func _run is required for any chiled class
        self.is_running=False

    def start_thread(self, chiled_threads:list=None):
        self.terminate = False
        # New Thread
        thread = Thread(target=self.run)
        add_report_ctx(thread)
        thread.start()
        if chiled_threads:
            for ct in chiled_threads:
                ct.start_thread()

    def terminate_thread(self,chiled_threads:list=None):
        self.terminate = True
        if chiled_threads: #list of objects contains self.terminate
            for ct in chiled_threads:
                ct.terminate_thread()


# Main DataAQ from CC_USB <<-- TDC
# Branch (Level 1) Classes
class DAQ:

    def __init__(self, name="TDC"):
        self.name = name
        self.size = settings.get_setting(setting="arr_size", target=self.name)
        self.type = np.float64
        self.init()
        self.init_prev_arr()
        self.bins_to_time()

    def init(self,):
        self.avg_hit_list = [0]  #0 is to init and will be omitted
        self.set_arr()
        self.set_channel_arr()

    def set_arr(self): #Also Clear
        self.arr = np.zeros(self.size, dtype=self.type)

    def init_prev_arr(self,): # Also Clear
        self.prev_arr = self.arr.copy()

    def set_channel_arr(self,):
        tot_channel_size=settings.get_setting("tot_nodch")
        self.channel_window_size = 4000 // (tot_channel_size + 2) # #*Potential bugus when the stream has smaller size
        channel_size=settings.get_setting("nodch", target=self.name)
        self.channel_arr = np.zeros([self.channel_window_size, channel_size], dtype=np.int32)

    def bins_to_time(self):
        self.channel = settings.get_setting("input_channel_number", target = self.name)
        self.slop = settings.get_setting("time_slop", target = self.name)
        self.offset = settings.get_setting("time_offset", target = self.name)
        self.time_resolution = settings.get_setting("time_resolution", target = self.name)
        self.tdc_t_shift = self.slop * self.channel + self.offset # unit in [ns]
        self.time_arr = self.time_resolution * np.arange(self.size, dtype=self.type) + self.tdc_t_shift #ns

    def get_tot_avg_hit(self, last=None):
        if last:
            last = -last
        else:
            last = 1 # excluding the first 0 element
        return np.average(self.avg_hit_list[last:]) if self.avg_hit_list else np.nan

    def auto_save(self):
        with open(self.name+"_temp.csv", 'w') as f:
            np.savetxt(f, self.arr)

    def save(self, file_path, info:dict):
        self._gen_header(info)
        file_path = file_path[:-4] + "_" + self.name + ".csv"
        with open(file_path, 'w') as fh:
            np.savetxt(fh, np.array([self.time_arr,self.arr]).T, delimiter=',', header=self.header, fmt='%.4f')
        # store the data_count_ar
        self.prev_arr = self.arr.copy() #Previous data arr

    def _gen_header(self, info:dict):
        self.header = "Time: " + str(datetime.datetime.today()) + '\n'
        for key, value in info.items():
            self.header += f"{key} : {value}\n"


# Branch (Level 1) classes
class Display: #* remove container

    def init_fig(self, figsize=None, dpi=90):
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi)

    # def add_handler(self, handler):
    #     self.handler = handler

    # def st_plot(self):
    #     self.handler.pyplot(self.fig)


