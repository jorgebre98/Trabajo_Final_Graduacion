import serial
import struct
import random
from Timer import RepeatedTimer
import threading 
import time

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False 
    
def Receive(port,num):
    packed = struct.pack('f',num)
    data = port.read(size=4)
    port.write(packed)
    data_r = struct.unpack('f',data)
    print('\nData receive: ',data_r[0],'\nData Transmit: ',num,flush=True)
    
def Data_collect(ser):
    pwm_value = round(random.uniform(0,4),4)
    data_receive = Receive(ser, pwm_value)

#Definicion puerto serial
serial_port = serial.Serial("/dev/ttyUSB0",
                            baudrate=115200,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE)

print('**********  Strarting********** ',flush=True)
Data_collect(serial_port)
rt = RepeatedTimer(0.02,Data_collect,serial_port)
try:
    time.sleep(10) # long running job
finally:
    rt.stop()
    
