from classes import Display


# Custom (Level 2) Clases
## Time Of Flight custom Class
class ToF(Display):

    def __init__(self,size=100, type=np.int64, figsize=[6,5]], dpi=120):
        Display().__init__()

        self.arr_size = size
        self.arr_type = type
        self.figsize = figsize
        self.dpi = dpi

        # Init Array from Container class:
        self.set_arr(size=self.arr_size, type=self.arr_type)

        # Init Figure from Display class:
        self.init_fig(figsize=self.figsize, dpi=self.dpi)
        self.line, = self.ax.plot(self.arr) 

        # Fig info:
        self.ax.set_title = "Time OF Flight"
        self.ax.set_xlabel = "Time (ns)"
        self.ax.set_ylabel = "Yeild (a.u.)"

    def _run(self):
        # Read TDC arr  
            ??
        # Update plot
        self.update(y_min=0.1)
        # plot
        self.st_plot()




## Monitor TOF
class Mtof_stream(Display):

    def __init__(self, size=(409, 8), type=np.int32, figsize=[4, 2], dpi=120):
        Display().__init__()

        # Init Array from Container class:
        self.set_arr(size, type)

        # Init Figure from Display class:
        self.init_fig(figsize=figsize, dpi=dpi)
        self.get_lines()

        # Fig info:
        self.ax.set_title = "Channels Data - 8 hits max."
        self.ax.set_xlabel = "Laser Shot (Updating ..)"
        self.ax.set_ylabel = "TDC Count"

        self.ax.set_ylim(-1, 2100)

    def get_lines(self,):
        self.line = []  #The name must be "line" so it stay compatible with Display class defaults
        for i in range(self.arr.shape[-1]):
            self.line.append(self.ax.plot(self.arr[:, i], label=f"CH# {i}"))
        
    def _run(self):
        # Read TDC arr  
            ??
        # Update plot
        self.update(y_min=-1)
        # plot
        self.st_plot()



## Monitor TOF
class Mtof_hits(Display):

    def __init__(self, size=100, type=np.float16, figsize=[4, 2], dpi=120):
        Display().__init__()

        # Init Array from Container class:
        self.set_arr(size, type)
        self.arr_indx

        # Init Figure from Display class:
        self.init_fig(figsize=figsize, dpi=dpi)
        self.line = self.ax.plot(self.arr)

        # Fig info:
        self.ax.set_title = "Average ions hit per laser shot"
        self.ax.set_ylabel = "hit/shot"
        self.ax.set_xlabel = "Time (updating ..)"

        self.ax.set_ylim(-0.5, 8.5)
        
    def _run(self):
        # Read TDC arr  
            ??
        self.arr[self.arr_indx] = ?? #TDC avg hit
        # Update plot
        self.update(y_min=-0.5)
        # plot
        self.st_plot()
        # update index
        self.arr_indx += 1
        if self.arr_indx >= self.arr.size:
            self.arr_indx = 0