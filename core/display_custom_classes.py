from core.classes import Display, Threading
from time import sleep
from settings.settings import settings
import numpy as np

## Time Of Flight custom Class
class ToF(Display, Threading):

    def __init__(self, tdcs_obj_list, figsize=[4,3], dpi=90, delay=1):
        self.auto_scale = True
        self.tdcs_obj_list = tdcs_obj_list
        self.delay = delay  # sec
        # Init Figure from Display class:
        self.init_fig(figsize=figsize, dpi=dpi)

        # init lines
        self.lines = []
        for tdc in self.tdcs_obj_list:
            line, = self.ax.plot(tdc.time_arr, tdc.arr, label=tdc.name) # time, arr : for each module
            self.lines.append(line)
        
        # init prev lines
        self.prev_lines = []
        for tdc in self.tdcs_obj_list:
            prev_line, = self.ax.plot(tdc.time_arr, tdc.prev_arr, label=tdc.name+'_prev') # time, arr : for each module
            prev_line.set_linestyle("None") #Invisible
            self.prev_lines.append(prev_line)

        # Fig info:
        self.ax.set_title("Time OF Flight")
        self.ax.set_xlabel("Time (ns)")
        self.ax.set_ylabel("Yeild (a.u.)")

        self.fig.legend()  # also you can do: self.ax.legend()

        self.ymax = 0

    def update(self,):
        for i, tdc in enumerate(self.tdcs_obj_list):
            self.lines[i].set_ydata(tdc.arr/tdc.arr.max()) #Normalization
            #self.ymax = np.max([self.ymax, tdc.arr.max()])
        #if self.auto_scale:
        #    self.ax.set_ylim(0.1, self.ymax*1.05)


    def _run(self):
        # Read TDC arr and update line plot  
        self.update()
        # Update plot scale
        
        # render to the st app
        #self.st_plot()
        sleep(self.delay)
        #print("R TOF")

    def show_prev_arr(self, ON=True):
        for i, tdc in enumerate(self.tdcs_obj_list):
            if ON:
                self.prev_lines[i].set_ydata(tdc.prev_arr/tdc.prev_arr.max())
                self.prev_lines[i].set_linestyle("--")  # Visible
            else:
                self.prev_lines[i].set_linestyle("None") # Invisible



## Monitor TOF
class Mtof_stream(Display, Threading):

    def __init__(self, tdcs_obj_list, figsize=[4, 2], dpi=90, delay=1):
        self.tdcs_obj_list = tdcs_obj_list
        self.delay = delay
        # Init Figure from Display class:
        self.init_fig(figsize=figsize, dpi=dpi)

        # init lines
        self.lines = []
        for tdc in self.tdcs_obj_list:
            sublines = []
            for arr in tdc.channel_arr.T:
                line, = self.ax.plot(arr) #list of lines
                sublines.append(line)
            self.lines.append(sublines)

        # Fig info:
        self.ax.set_title("Channels Data")
        self.ax.set_xlabel("Laser Shot (Updating ..)")
        self.ax.set_ylabel("TDC Count")

        self.ax.set_ylim(-10, 4100)

    def update(self,):
        # Read TDC arr and update line plot  
        for i, tdc in enumerate(self.tdcs_obj_list):
            for j, line in enumerate(self.lines[i]):
                line.set_ydata(tdc.channel_arr[:tdc.channel_window_size, j])

    def _run(self):
        self.update()
        # plot
        #self.st_plot()
        sleep(self.delay)
        #print("R Stream")



## Monitor TOF (avg Hit/shot)
class Mtof_hits(Display, Threading):

    def __init__(self,tdcs_obj_list,figsize=[4,2], dpi=90, delay=1, fixed_hit_arr_size=100):        
        self.tdcs_obj_list = tdcs_obj_list
        self.delay = delay  # sec
        self.fixed_hit_arr_size = fixed_hit_arr_size
        # Init Figure from Display class:
        self.init_fig(figsize=figsize, dpi=dpi)

        self.init_fixed_hit_arr()
        
        # init lines
        self.lines = []
        for tdc in self.tdcs_obj_list:
            line, = self.ax.plot(tdc.fixed_hit_arr, label=tdc.name) # time, arr : for each module
            self.lines.append(line)

        # Fig info:
        self.ax.set_title("Average ions hit per laser shot")
        self.ax.set_ylabel("hit/shot")
        self.ax.set_xlabel("Time (updating ..)")

        self.ax.set_ylim(-1, 9)
        self.ax.set_xlim(0, self.fixed_hit_arr_size)
        self.ax.legend()  # also you can do: self.ax.legend()

    def init_fixed_hit_arr(self,):
        self.index = 0
        for tdc in self.tdcs_obj_list:
            tdc.fixed_hit_arr = np.zeros(self.fixed_hit_arr_size, dtype=np.int16)
    

    def update(self,):
        # Read TDC arr and update line plot  
        for i, tdc in enumerate(self.tdcs_obj_list):
            tdc.fixed_hit_arr[self.index] = tdc.avg_hit_list[-1]
            self.lines[i].set_ydata(tdc.fixed_hit_arr)      
        # Update plot scale
        self.index += 1
        if self.index == self.fixed_hit_arr_size:
            self.index = 0 

    def _run(self):
        self.update()
        #print("R hit")
        # render to the st app
        #self.st_plot()
        sleep(self.delay)