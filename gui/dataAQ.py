from core.daq_custom_classes import DCounter
from core.display_custom_classes import ToF, Mtof_stream, Mtof_hits
from interface.read_out import read_out

class Main:

    def __init__(self,):
        self.init_var()
        self.init_obj()

    def init_var(self,):

        self.is_tdc_connected = False
        self.is_running = False

        self.tof_fig_size = [6, 5]
        self.tof_dpi = 120

        self.s_fig_size = [4, 2]
        self.s_dpi = 120

        self.h_fig_size = [4, 2]
        self.h_dpi = 120

    
    def init_obj(self):
        read_out.init()

        self.dcounter = DCounter()
        
        self.tof = Tof(self.dcounter.tdcs_obj_list, 
                    figsize=self.tof_fig_size, dpi=self.tof_dpi)
        
        self.mtof_stream = Mtof_stream(self.dcounter.tdcs_obj_list, 
                    figsize=self.s_fig_size, dpi=self.s_dpi)
        
        self.mtof_hit = Mtof_hits(self.dcounter.tdcs_obj_list, 
                    figsize=self.h_fig_size, dpi=self.h_dpi)


    def reload(self,): #update settings
        if self.is_tdc_connected == False:
            self.__init__()

    def add_handler(self, tof_hand, s_hand, h_hand)
        # A figure handler must be added
        self.tof.add_handler(tof_hand)
        self.mtof_stream.add_handler(s_hand)
        self.mtof_hit.add_handler(h_hand)

        
    def run(self):
        if self.is_tdc_connected == False:
            self.TDC_connect()
        # Main thread
        self.dcounter.start_thread(
            chiled_threads=[self.tof, self.mtof_stream, self.mtof_hit]
            )
        # ^ now all display threads will start once dcounter start
        self.is_running = True

    def stop(self):
        self.dcounter.terminate_thread(
            chiled_threads=[self.tof, self.mtof_stream, self.mtof_hit]
            )
        self.is_running = False

    def save(self, file_path, info:dict):
        self.dcounter.save(file_path, info:dict)


    def clear(self):
        self.dcounter.clear()
        for d in [self.tof, self.mtof_stream, self.Mtof_hit]:
            d.update()
            d.st_plot()


    def TDC_connect(self):
        read_out.connect()
        self.is_tdc_connected = True

    def TDC_close(self):
        if self.is_tdc_connected:
            read_out.close()
            self.is_tdc_connected = False




