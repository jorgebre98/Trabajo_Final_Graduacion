## Tecnológico de Costa Rica
### Autor: Jorge Andrés Brenes Alfaro
## Data_collection.py

#********** Libraries **********#
import csv
import time
import serial
import random
import keyboard
import threading 
import numpy as np
from struct import pack, unpack

# ********************************** Transmit/Receive Class **********************************# 
class TransmitReceive:
    def __init__(self, serial_port):
        self.port = serial_port
        self.pwm = None
        self.angle = None
        self.lantency = None
        self.contador = 0
        self.values = [["LATENCY","PWM_VALUE","ANGLE"]]

    def Transmit_Receive (self):
        self.pwm_ramp_step()
        if self.port.inWaiting() > 0:
            # Send 2 bytes
            packed = pack('!h',self.pwm)
            ini = time.time()
            self.port.write(packed)
            
            # Receive 4 bytes
            data = self.port.read(size=4)
            self.latency = time.time()-ini
            self.angle = unpack('!i',data)
            self.values.append([self.latency, self.pwm, self.angle[0]])
            #print('Transmit: {0} and Receive: {1}'.format(self.pwm,self.angle[0]))

    def reset(self):
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()

    def csv_doc(self):
        with open('Data_Collect.csv','w', newline='') as file:
            doc = csv.writer(file, delimiter=',')
            doc.writerows(self.values)

    def pwm_ramp_step(self):
        #self.pwm = 125+int(random.uniform(0,4)/4*125)
        #if self.contador <= 500:
        #    self.contador +=1
        #    self.pwm = self.contador
         
        if self.contador <= 350:
            self.contador +=1
        #else:
            #self.contador = 0
        self.pwm = self.contador
         
    def turn_off(self):
        self.pwm = 0
        self.port.write(pack('!i',self.pwm))
