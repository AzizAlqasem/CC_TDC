from classes import DAQ



class DCounter(DAQ):

    def __init__(self, name, size, type):
        DAQ.__init__(name):
        self.set_arr(size, type)
        self.init()


