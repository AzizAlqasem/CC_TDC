import matplotlib.pyplot as plt
import numpy as np
from threading import Thread



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

    def start_thread(self,):
        self.terminate = False
        # New Thread
        Thread(target=self.run).start()

    def terminate_thread(self,):
        self.terminate = True 


# Main DataAQ from CC_USB <<-- TDC
# Branch (Level 1) Classes
class DAQ:

    def __init__(self, name="TDC"):
        self.name = name
        self.size = settings.set_setting(key="arr_size", target=self.name)
        self.type = np.int64
        self.init_prev_arr()
        self.bins_to_time()
        #Container.__init__() #will be taken by DCounter object

    def init(self,):
        self.avg_hit_list = []
        self.set_arr()
        self.set_channel_arr()
    
    def init_prev_arr(self,): # Also Clear
        self.prev_arr = self.arr.copy()
    
    def set_arr(self): #Also Clear
        self.arr = np.zeros(self.size, dtype=self.type)

    def set_channel_arr(self,):
        channel_size=settings.get_setting("nodch", target=self.name)
        self.channel_arr = np.zeros([1, channel_size], dtype=np.int32)

    def bins_to_time(self):
        channel = settings.get_setting("input_channel_number", target = self.name)
        slop = settings.get_setting("time_slop", target = self.name)
        offset = settings.get_setting("time_offset", target = self.name)
        time_resolution = settings.get_setting("time_resolution", target = self.name)
        self.tdc_t_shift = slop * channel + offset # unit in [ns]
        self.time_arr = time_resolution * np.arange(self.size, dtype=self.type) + self.tdc_t_shift #ns

    def auto_save(self):
        with open(self.name+"_temp.csv", 'w') as f:
            np.savetxt(f, self.arr)
          
    def save(self, file_path, info:dict):
        self._gen_header(info)
        with open(file_path, 'w') as fh:
            np.savetxt(fh, np.array([self.time_ar,self.arr]).T, delimiter=',', header=self.header)
        # store the data_count_ar
        self.prev_arr = self.arr.copy() #Previous data arr

    def _gen_header(self, info:dict):
        self.header = "Time: " + str(datetime.datetime.today()) + '\n'
        for key, value in info.items():
            self.header += f"{key} : {value}\n"


# Branch (Level 1) classes
class Display(Container): #* remove container
    def __init__(self,):
        Container().__init__()
        #self.auto_scale = False

    def init_fig(self, figsize=None, dpi=90):
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi)
        #self.line, = self.ax.plot(self.arr) 
        # ^ The arr is NOT set by default, so init arr first
        # ^ Also the array could by n-dim

    def add_handler(self, handler):
        self.handler = handler

    def st_plot(self):
        self.handler.pyplot(self.fig)

    def update(self, y_min=0): #* Remove This
        if type(self.line) is list:
            for i in range(len(line)):
                self.line[i].set_ydata(self.arr[:,i])
        else: #One line
            self.line.set_ydata(self.arr)
            if self.auto_scale:
                self.ax.set_ylim(y_min, max(self.arr)*1.05)

    def clear(self, ):
        self.set_arr()
        self.update()


