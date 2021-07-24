from classes import Display, Threading
from time import sleep

## Time Of Flight custom Class
class ToF(Display, Threading):

    def __init__(self, tdcs_obj_list, figsize=[6,5], dpi=120, delay=1):
        self.auto_scale = False
        self.tdcs_obj_list = tdcs_obj_list
        self.delay = delay  # sec
        # Init Figure from Display class:
        self.init_fig(figsize=figsize, dpi=dpi)

        # init lines
        self.lines = []
        for tdc in self.tdcs_obj_list:
            line, = self.ax.plot(tdc.time_arr, tdc.arr, label=tdc.name) # time, arr : for each module
            self.lines.append(line)

        # Fig info:
        self.ax.set_title = "Time OF Flight"
        self.ax.set_xlabel = "Time (ns)"
        self.ax.set_ylabel = "Yeild (a.u.)"

        self.fig.legend()  # also you can do: self.ax.legend()


    def _run(self):
        # Read TDC arr and update line plot  
        for i, tdc in enumerate(self.tdcs_obj_list):
            self.lines[i].set_ydata(tdc.arr)
        # Update plot scale
        if self.auto_scale:
            self.ax.set_ylim(0.1, max(self.arr)*1.05)
        # render to the st app
        self.st_plot()
        sleep(self.delay)



## Monitor TOF
class Mtof_stream(Display, Threading):

    def __init__(self, tdcs_obj_list, figsize=[4, 2], dpi=120, delay=1):
        self.tdcs_obj_list = tdcs_obj_list

        # Init Figure from Display class:
        self.init_fig(figsize=figsize, dpi=dpi)
        self.get_lines()

        # init lines
        self.lines = []
        for tdc in self.tdcs_obj_list:
            line, = self.ax.plot(tdc.channel_arr) # time, arr : for each module
            self.lines.append(line)

        # Fig info:
        self.ax.set_title = "Channels Data"
        self.ax.set_xlabel = "Laser Shot (Updating ..)"
        self.ax.set_ylabel = "TDC Count"

        self.ax.set_ylim(-1, 2100)
        
    def _run(self):
        # Read TDC arr and update line plot  
        for i, tdc in enumerate(self.tdcs_obj_list):
            self.lines[i].set_ydata(tdc.channel_arr)
        # plot
        self.st_plot()
        sleep(self.delay)



## Monitor TOF (avg Hit/shot)
class Mtof_hits(Display, Threading):

    def __init__(self,tdcs_obj_list,figsize=[6,5], dpi=120, delay=1)        
        self.tdcs_obj_list = tdcs_obj_list
        self.delay = delay  # sec
        # Init Figure from Display class:
        self.init_fig(figsize=figsize, dpi=dpi)
        
        # init lines
        self.lines = []
        for tdc in self.tdcs_obj_list:
            line, = self.ax.plot(tdc.avg_hit_list label=tdc.name) # time, arr : for each module
            self.lines.append(line)

        # Fig info:
        self.ax.set_title = "Average ions hit per laser shot"
        self.ax.set_ylabel = "hit/shot"
        self.ax.set_xlabel = "Time (updating ..)"

        self.ax.set_ylim(-0.5, 8.5)

        self.fig.legend()  # also you can do: self.ax.legend()

        
    def _run(self):
        # Read TDC arr and update line plot  
        for i, tdc in enumerate(self.tdcs_obj_list):
            self.lines[i].set_ydata(tdc.avg_hit_list)
        # Update plot scale
        self.ax.set_xlim(0, int(len(tdc.avg_hit_list)*1.05))
        # render to the st app
        self.st_plot()
        sleep(self.delay)