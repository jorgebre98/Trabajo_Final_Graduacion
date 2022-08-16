## Tecnológico de Costa Rica
### Autor: Jorge Andrés Brenes Alfaro
## Data_collection.py

# The code presented allows an NVIDIA Jetson TX2 communicate with a PSoC 
# with the purpose of collect data from a Péndulo amortiguado a hélice (PAHM) plant.

#Libraries
import time
import serial
import struct
import random
import xlsxwriter
import numpy as np
from Timer import *

# ********************************** Step Function **********************************#
def step_function(A,t):
    u = (t >= 0)*A
    return u

# ********************************** Ramp Function **********************************#
def ramp_function(A,t):
    r = t*step_function(A,t)
    return r

# *********************** Function to create .xlsx archives *************************#
def archivo_excel(values):
    archive = xlsxwriter.Workbook("Data_collection.xlsx")
    hoja = archive.add_worksheet()
    names = ['Latencia','Entrada','Ángulo']
    for j in range(len(names)):
        hoja.write(0,j,names[j])

    for j in range(len(values)):
        for i in range(len(values[j])):
            hoja.write(j+1,i,values[j][i]) # row, col, data
    archive.close()

# ********************************** Data Transmission and Reception **********************************#
def Transmit_Receive(port,num):
    packed = struct.pack('f',num)
    ini = time.time()
    port.write(packed)
    data = port.read(size=4)
    latencia = time.time()-ini
    data_r = struct.unpack('f',data)
    return data_r[0], latencia

def Data_collect(ser):
    pwm_value = round(random.uniform(0,4),4)
    data_receive, latencia = Transmit_Receive(ser, pwm_value)
    print('\nData_transmit: ', pwm_value,'\nData receive: ',data_receive,flush=True)
    return  [latencia,pwm_value,data_receive]
    

# ****** ***** Definicion del puerto ****** *******
serial_port = serial.Serial("/dev/ttyTHS2",
                            baudrate=115200,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE)
time.sleep(0.02)


#star, end, sampling = -2,10,0.02
#tiempo = np.concatenate([np.arange(star,end,sampling), np.zeros(1000)])
#Amplitude = round(random.uniform(0,4),4)
#step = step_function(Amplitude,tiempo)
#r = ramp_function(Amplitude,tiempo)
#print('\r\nAmplitud: ',Amplitude,'\r\n', flush = True)


print('************ Starting *************', flush=True)
rt = RepeatedTimer(0.02, Data_collect, serial_port) # No need of rt.start()
try:
    time.sleep(10) # long running job
finally:
    rt.stop()
    archivo_excel(rt.values)
serial_port.close()
