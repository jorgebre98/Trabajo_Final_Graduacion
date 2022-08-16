import serial
import struct
import random
from Timer import *
   
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
    
