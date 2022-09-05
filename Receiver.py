import serial
import struct
import random
from Timer import *

# FUntion to receive values
def Receive(port):
    data = port.read(size=4)
    data_r = struct.unpack('i',data)
    print('\nData receive: ', data_r[0], flush=True)
    
# SERIAL PORT DEFINE
serial_port = serial.Serial("/dev/ttyTHS2",baudrate=115200,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)

print('**********  Starting ********** ',flush=True)
rt = RepeatedTimer(0.02,Receive,serial_port)
try:
    time.sleep(2) # long running job
finally:
    rt.stop()
    
