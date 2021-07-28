"""This module is to interface with the CC-USB using 
the pyxxusb which is a pyhton wrape to the main C/C++
module made by the manufacture.

"""
try:
    from interface.pyxxusb import _pyxxusb as pycc # Here it is used only for comunicationg with the CC-USB
except Exception as e:
    print(e)
    print("pyxxusb lib works only with python 32bit")
    print("The PC should be connected to the cc-usb")

from interface._tools import generate_stack, stack_as_longArray


BUFFER_SIZE = {
    0 : 4096,
    1 : 2048,
    2 : 1024,
    3 : 512,
    4 : 256,
    5 : 128,
    6 : 64,
    7 : 1
}


class CC_USB:

    def __init__(
        self, commands=None, stack=None, stack_type=2, time_out_ms=100,
        LAM=0, trig_delay_us=100, buffer_opt=0, marker=True):

        self.time_out_ms = time_out_ms
        self.stack_type = stack_type
        self.LAM = LAM
        self.trig_delay_us = trig_delay_us
        self.buffer_opt = buffer_opt

        if not commands and not stack:
            raise ValueError("Commands or Stack must be provided!")

        if commands:
            self.stack_ar = generate_stack(*commands, marker=marker)
        else:
            if type(stack) == type(pycc.new_longArray(1)):
                self.stack_ar = stack
            elif type(stack) == list:
                self.stack_ar = stack_as_longArray(stack)
            else:
                raise TypeError("The stack type is not suported. Consider using list or longArray")

        self.data_shortArray = pycc.new_shortArray(8192) # 32bit PC reads 8192 buff size
        
        self.cc_dev = pycc.device_open()

    def connect_to_module(self, module:object):
        module.cc_dev = self.cc_dev

    def stack_write(self):
        bytes_sent = pycc.xxusb_stack_write(self.cc_dev, self.stack_type, self.stack_ar)
        if bytes_sent < 0 :
            print("Failure! The stack is not sent to the cc-usb!")
        return bytes_sent

    def set_trigger_delay(self,):
        q = pycc.new_int_p()
        x = pycc.new_int_p()
        bytes_written = pycc.CAMAC_write(self.cc_dev, 25, 2, 16, self.trig_delay_us, q, x)
        if bytes_written < 0:
            print("Failure! write_LAM_mask failed")
        return bytes_written, pycc.int_p_value(q), pycc.int_p_value(x)

    def set_buffer_size(self,):
        """
        buffer_opt
        0   4096
        1   2048
        """
        q = pycc.new_int_p()
        x = pycc.new_int_p()
        bytes_written = pycc.CAMAC_write(self.cc_dev, 25, 1, 16, self.buffer_opt, q, x)
        if bytes_written < 0:
            print("Failure! set_buffer_size failed")
        return bytes_written, pycc.int_p_value(q), pycc.int_p_value(x)

    def set_data_aq_mode(self, ON:bool):
        bytes_written = pycc.xxusb_register_write(self.cc_dev, 1, int(ON))
        if bytes_written < 0:
            print("Failure! Changing DataAq mode is failed")
        return bytes_written

    def write_LAM_mask(self,):
        q = pycc.new_int_p()
        x = pycc.new_int_p()
        bytes_written = pycc.CAMAC_write(self.cc_dev, 25, 9, 16, self.LAM, q, x)
        if bytes_written < 0:
            print("Failure! write_LAM_mask failed")
        return bytes_written, pycc.int_p_value(q), pycc.int_p_value(x)

    def bulk_read(self):
        byets_receved = pycc.xxusb_bulk_read(self.cc_dev, self.data_shortArray, 
            8192, self.time_out_ms) # 32-bit PC reads 8192 buff size
        if byets_receved<0:
            print("No Data to read ..")
            return None
        else:
            data_size = byets_receved // 2
            return [pycc.shortArray_getitem(self.data_shortArray, i) for i in range(data_size)]
        
    
    def drain_FIFO_data(self):
        loop = 0
        byets_receved = 1
        while byets_receved > 0 and loop < 100:
            byets_receved = pycc.xxusb_bulk_read(self.cc_dev, self.data_shortArray, 
                                            8192, self.time_out_ms)
            loop += 1

    def close(self,):
        self.drain_FIFO_data()
        self.set_data_aq_mode(ON=False)
        self.drain_FIFO_data()
        pycc.xxusb_device_close(self.cc_dev)



class CC_Module:
    
    def __init__(self, module_slot_number):
        self.N = module_slot_number

    def disable_LAM(self,):
        q = pycc.new_int_p()
        x = pycc.new_int_p()
        d = pycc.new_long_p()
        bytes_written = pycc.CAMAC_read(self.cc_dev, self.N, 0, 24, d, q, x)
        if bytes_written < 0:
            print("Failure! disable_LAM failed")
        return bytes_written, pycc.int_p_value(q), pycc.int_p_value(x)

    def clear_LAM(self, f=9):
        q = pycc.new_int_p()
        x = pycc.new_int_p()
        d = pycc.new_long_p()
        bytes_written = pycc.CAMAC_read(self.cc_dev, self.N, 0, f, d, q, x)
        if bytes_written < 0:
            print("Failure! clear_LAM failed")
        return bytes_written, pycc.int_p_value(q), pycc.int_p_value(x)







    

    
    