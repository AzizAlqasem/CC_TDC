from core.daq_custom_classes import DCounter
from core.display_custom_classes import ToF, Mtof_hits
from interface.read_out import read_out
from settings.settings import settings
from pylablib.devices import Thorlabs


class Main:

    def __init__(self,):
        self.init_var()
        self.init_obj()
        self.init_motors()

    def init_var(self,):

        self.is_tdc_connected = False
        self.is_running = False
        self.is_scanning = False

        self.tof_fig_size = [14, 8]
        self.tof_dpi = 140

        # self.s_fig_size = [4, 2]
        # self.s_dpi = 80 #120

        self.h_fig_size = [4, 3]
        self.h_dpi = 60 #120

        self.y_scale = 'linear' # log
        self.xlim = (0.0, 150.0)
        self.ylim = (1e-8, 1.0)

        self.live_plot = True

        # Motor constants:
        self.STEP_SIZE_PER_DEGREE = 1920.1274919 #600_000/312  #Might be different for different motors
        self.current_motor_pos = 0.0 # angle
        # self.scan_angles = [118.7053, 111.9327, 118.0158, 114.4282, 115.1718, 108.9222, 114.1762, 116.6148, 112.6147, 111.0832, 114.9257, 116.0198, 116.8508, 117.6688, 110.4947, 114.3022, 109.2502, 117.9003, 111.3707, 113.0142, 108.2412, 110.0397, 109.7287, 117.3198, 111.5127, 113.7942, 110.9382, 109.8852, 115.6583, 111.2277, 113.2767, 117.7848, 114.5532, 110.1927, 116.7328, 118.1313, 112.3447, 113.9222, 112.7487, 108.0652, 107.8862, 116.1393, 114.6777, 116.9683, 115.0488, 115.8998, 109.0872, 115.2938, 108.4147, 114.0497, 109.4117, 118.4763, 113.1457, 113.6662, 108.7552, 114.8017, 116.4963, 117.4363, 111.6537, 117.2028, 116.3778, 110.3447, 110.6437, 111.7937, 118.3613, 113.5367, 118.5908, 112.0707, 117.0858, 116.2588, 115.4158, 108.5862, 117.5523, 112.4802, 115.7793, 113.4072, 118.2463, 109.5712, 112.8817, 115.5373, 112.2082, 110.7917]
        self.round_counter = 0 # round scan counter for LIED exper. (temp)

    def init_obj(self):
        read_out.init()

        self.dcounter = DCounter()

        self.tof = ToF(self.dcounter.tdcs_obj_list,
                    figsize=self.tof_fig_size, dpi=self.tof_dpi)

        # self.mtof_stream = Mtof_stream(self.dcounter.tdcs_obj_list,
        #             figsize=self.s_fig_size, dpi=self.s_dpi)

        self.mtof_hit = Mtof_hits(self.dcounter.tdcs_obj_list,
                    figsize=self.h_fig_size, dpi=self.h_dpi)

    def init_motors(self,):# Init any moter connected to PC such as the rotation stage of the half wave plate
        self.devices = Thorlabs.list_kinesis_devices()
        print("Found devices: ", self.devices)
        if self.devices:
            self.motor_sn = self.devices[0][0]
            self.motor = Thorlabs.KinesisMotor(self.motor_sn)
            self.motor.home()
            self.is_motor_connected = True
            print("Motor successfuly connected: ", self.motor_sn)
        else:
            print("No motor found!")
            self.is_motor_connected = False

    def reload(self,): #update settings
        if self.is_tdc_connected == False:
            self.__init__()
            settings.__init__()


    def add_handler(self, tof_hand, s_hand, h_hand):
        # A figure handler must be added
        self.tof.add_handler(tof_hand)
        # self.mtof_stream.add_handler(s_hand)
        self.mtof_hit.add_handler(h_hand)


    def run(self):
        if self.is_tdc_connected == False:
            self.TDC_connect()
        # Main thread
        if self.is_running == False:
            self.dcounter.start_thread(
                chiled_threads=[self.tof, self.mtof_hit]#[self.tof, self.mtof_stream, self.mtof_hit]
                )
            # ^ now all display threads will start once dcounter start
            self.is_running = True
        else:
            print("The app is already running!")

    def stop(self):
        self.dcounter.terminate_thread(
            chiled_threads=[self.tof, self.mtof_hit]#[self.tof, self.mtof_stream, self.mtof_hit]
            )
        self.is_running = False
        print("stop")


    def clear(self):
        self.dcounter.clear()
        self.mtof_hit.init_fixed_hit_arr()
        for d in [self.tof, self.mtof_hit]:#[self.tof, self.mtof_stream, self.mtof_hit]:
            d.update()
            #d.st_plot()


    def TDC_connect(self):
        read_out.connect()
        self.is_tdc_connected = True

    def TDC_close(self):
        if self.is_tdc_connected:
            read_out.close()
            self.is_tdc_connected = False


    # tools:
    def adj_y_scale(self, y_scale):
        if y_scale != self.y_scale:
            self.tof.ax.set_yscale(y_scale)
            self.y_scale = y_scale

    def adj_xlim(self, xlim):
        if xlim != self.xlim:
            self.tof.ax.set_xlim(*xlim)
            self.xlim = xlim
    def adj_ylim(self, ylim):
        if ylim != self.ylim:
            self.tof.ax.set_ylim(*ylim)
            self.ylim = ylim


