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
        self.values = []

    def Transmit_Receive (self):
        self.create_pwm()
        if self.port.inWaiting() > 0:
            packed = pack('!i',self.pwm)
            ini = time.time()
            self.port.write(packed)
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

    def create_pwm(self):
        #self.pwm = 125+int(random.uniform(0,4)/4*125)
        if self.contador <= 145:
            self.contador +=1
            self.pwm = self.contador

    def turn_off(self):
        self.pwm = 0
        self.port.write(pack('!i',self.pwm))
        #self.contador = -1
        #self.Transmit_Receive()
        self.port.close()

# ********************************** Input Class **********************************# 
class Inputs:
    def __init__(self,amplitude, time):
        self.A = amplitude
        self.t = time
        self.contador = 0

# Step Function
    def step_function(self):
        u = (self.t >= 0)*self.A
        return u

# Ramp Function
    def ramp_function(self):
        r = self.t*self.step_function()
        return r

    def manual(self):
        if keyboard.read_key() == 'a' or keyboard.read_key() == 'A':
            self.contador += 5
            print('Valor del contador: ', contador, flush = True)
        elif keyboard.read_key() == 'd' or keyboard.read_key() == 'D':
            self.contador -= 5
            print('Valor del contador: ', contador, flush = True)
        TransmitReceive.pwm = contador


# ********************************** Timer Class **********************************#
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
