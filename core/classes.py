import matplotlib.pyplot as plt
import numpy as np
import streamlit as st #?



# General (Level 0) Class
class Container:

    def __init__(self):
        self.terminate = False # Terminate running Thread

        #Check the status of run loop
        self.is_running = False 


    def set_arr(self, size=100, type=np.int64): #Also Clear
        self.arr = np.zeros(size, dtype=type)

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
class DAQ(Container):

    def __init__(self, name="TDC"):
        self.name = name
        Container.__init__()

    def init(self,):
        self.tot_laser_shot = 0
        self.avg_hit_list = []
    
    def init_prev_arr(self,): # Also Clear
        self.prev_arr = self.arr.copy()
    
    def get_tot_avg_hit(self):
        if self.avg_hit_list:
            return np.average(self.avg_hit_list)
        return np.nan

    def bins_to_time(self, channel,  slop, offset, time_resolution):
        self.tdc_t_shift = slop * channel + offset # unit in [ns]
        self.time_ar = time_resolution * np.arange(2048, dtype=np.float64) + self.tdc_t_shift #ns

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
class Display(Container):
    def __init__(self,):
        Container().__init__()
        self.auto_scale = False

    def init_fig(self, figsize=None, dpi=90):
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi)
        #self.line, = self.ax.plot(self.arr) 
        # ^ The arr is NOT set by default, so init arr first
        # ^ Also the array could by n-dim

    def add_handler(self, handler):
        self.handler = handler

    def st_plot(self):
        self.handler.pyplot(self.fig)

    def update(self, y_min=0):
        if type(self.line) is list:
            for i in range(len(line)):
                self.line[i].set_ydata(self.arr[:,i])
        else: #One line
            self.line.set_ydata(self.arr)
            if auto_scale:
                self.ax.set_ylim(y_min, max(self.arr)*1.05)

    def clear(self, ):
        self.set_arr()
        self.update()


