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
import numpy as np
from struct import pack, unpack

# ********************************** Transmit/Receive Class **********************************# 
class TransmitReceive:
    def __init__(self, serial_port, tiempo):
        self.port = serial_port
        self.pwm = None
        self.angle = None
        self.lantency = None
        self.tiempo = tiempo
        self.contador = 0
        self.values = []

    def Transmit_Receive (self):
        self.pwm = self.pwm_ramp_step() # Call input value to the PWM.
        if self.port.inWaiting() > 0:
            #       Send 2 bytes.
            packed = pack('!h',self.pwm)
            ini = time.time()
            self.port.write(packed)
            
            #       Receive 4 bytes.
            data = self.port.read(size=4)
            self.latency = time.time()-ini
            self.angle = unpack('!i',data)

            self.values.append(self.tiempo[contador], self.latency, self. pwm, self.angle[0])
            self.contador += 1

        def pwm_ramp_step(self):
            if self.amplitude <= 350:
                self.amplitude +=1
            return self.amplitude
    
    
    def reset(self):
        #   Clean transmit and receive buffers.
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()
        
    def turn_off(self):
        self.pwm = 0
        self.port.write(pack('!i',self.pwm))

    def normalizer(self):
        self.values = np.array(self.values)
        new_values = []
        
        # Normalize pwm values between 0 and 1
        for c in self.values[:,2]
            new_values.append((c-np.min(values))/(np.max(values)-np.min(values)))
        self.values[:,2] = new_values

        # Convert angle values of degrees to radians
        new_values = []
        for c in self.values[:,3]:
            new_values.append(c*np.pi/180)
        self.values[:,3] = new_values


    def csv_doc(self):
        name  = str(input('Nombre del documento: '))
        self.normalize()
        with open(name, 'w', newline='') as file:
            doc = csv.writer(file, delimiter=',')
            doc.writerows([['Time (ms)', 'Latencia (s)', 'PWM Value', 'Angle (rads)']])
            doc.writerows(self.values)        
