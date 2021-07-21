from classes import DAQ


#* it has some reptition with DAQ!
class DCounter(DAQ): 

    def __init__(self, name, size, type, auto_save_delay=10):
        self.name = name
        self.size = size
        self.type = type
        self.auto_save_delay = auto_save_delay
        DAQ.__init__(name):

        self.clear()
        self.init_prev_arr()

    def clear(self):
        self.set_arr(self.size, self.type)
        self.init()
        self.loop_counter = 0
    
    def _run(self,):
        # get data fron TDC
        ???
        # update 
        self.arr += ?data_from_TDC?
        self.avg_hit_list.append(??)
        self.tot_laser_shot += ??
        
        if self.loop_counter % self.auto_save_delay:
            self.auto_save()
        
        self.loop_counter += 1



