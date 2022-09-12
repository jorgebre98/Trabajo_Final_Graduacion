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
        self.pwm = 0
        self.angle = None
        self.lantency = None
        self.contador = 0
        self.values = np.array([])#['Latencia (s)', 'PWM Value', 'Angle (°)']]

    def Transmit_Receive (self):
        # Call input value to the PWM.
        if self.port.inWaiting() > 0:
            #       Send 2 bytes.
            packed = pack('!h',self.pwm)
            ini = time.time()
            self.port.write(packed)
            
            #       Receive 4 bytes.
            data = self.port.read(size=4)
            self.latency = time.time()-ini
            self.angle = unpack('!i',data)
            np.append(self.values,[self.latency, self. pwm, self.angle[0]],axis=0)
            print('PWM: {0}, Recibido: {1}.'.format(self.pwm,self.angle[0]))

    def pwm_ramp_step(self):
        if self.contador <= 1300:
            self.contador += 1
        self.pwm = self.contador
    
    def pwm_setvalue(self, value):
        value = int(value)
        if value <= 1300:
            self.pwm = value
        else:
            self.pwm = 1300
    
    def reset(self):
        #   Clean transmit and receive buffers.
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()
        
    def turn_off(self):
        self.pwm = 0
        self.port.write(pack('!i',self.pwm))

    
    def normalizer(self):
        #self.values = np.array(self.values)
        new_values = np.array([])
        
        # Normalize pwm values between 0 and 1
        for c in self.values[:,1]:
            np.append(new_values,(c-1000)/1000)
        self.values[:,1] = new_values
    
    def csv_doc(self, filename):
        self.normalizer()
        with open(filename, 'w', newline='') as file:
            doc = csv.writer(file, delimiter=',')
            doc.writerows([['Latencia (s)', 'PWM Value', 'Angle (°)']])
            doc.writerows(self.values)
            
