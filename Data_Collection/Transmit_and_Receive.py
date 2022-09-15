# Copyright (C) 2022 Jorge Brenes Alfaro.
# EL5617 Trabajo Final de Graduación.
# Escuela de Ingeniería Electrónica.
# Tecnológico de Costa Rica.

#   This file is responsible for transmit and receive data from the PAHM. For the generation
#   of data, 2 bytes corresponding to the value of the PWM are sent and it receives 4 bytes
#   corresponding to the value of the angle. The duration time of transmitting and receiving
#   the data is also saved. With these 3 values, a .csv file is created that will be used to train
#   the mimetic neural network.

#********** Libraries **********#
import csv
import time
import serial
import tkinter
import numpy as np
from struct import pack, unpack

# ********************************** Transmit/Receive Class **********************************# 
class TransmitReceive:
    def __init__(self, serial_port):
        self.port = serial_port
        self.pwm = 0.0
        self.angle = 0
        self.lantency = 0
        self.contador = 0
        self.cont = 0
        self.values = np.array([[0,0,0]])#[[0,0,0]]

    def denormalizePWM(self,normalizedValue):
        return int(normalizeValue*1000+1000)

    def Transmit_Receive (self):
        #       Send 2 bytes
        if np.isscalar(self.pwm):
            pwmval=self.pwm
        else:          
            if self.contador>=len(self.pwm):
                self.contador=0
            else:
                self.contador+=1
                  
            pwmval=self.pwm[self.contador]
                
        packed = pack('!h',self.denormalizePWM(pwmval))
                
        ini = time.time()
        self.port.write(packed)
        
        if self.port.inWaiting() > 0:
            #       Receive 4 bytes.
            data = self.port.read(size=4)
            self.latency = time.time()-ini
            self.angle = unpack('!i',data)

            #       Save latency, transmit and receive data
            val = np.array([[self.latency, pwmval, self.angle[0]*0.4]])
            self.values = np.append(self.values,val, axis=0)
   
    def reset(self):
        #   Clean transmit and receive buffers.
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()
        
    def turn_off(self):
        self.pwm = 0
        self.port.write(pack('!i',self.pwm))

    def pwm_ramp_step(self):
        if self.contador <= 1220:
            self.contador += 1
        self.pwm = (self.contador-1000)/1000.0
    
    def pwm_set_safe_value(self, value):
        self.pwm=np.min(value,0.25)
        
    
    def csv_doc(self, filename):
        with open(filename, 'w', newline='') as file:
            doc = csv.writer(file, delimiter=',')
            doc.writerows([['Latencia (s)', 'PWM Value', 'Angle (°)']])
            doc.writerows(self.values)
            
