#   Copyright (C) 2022 Jorge Brenes Alfaro.
#   EL5617 Trabajo Final de Graduación.
#   Escuela de Ingeniería Electrónica.
#   Tecnológico de Costa Rica.

#   This file contains the inputs to the pwm's value.

import keyboard
import numpy as np

# ********************************** Input Class **********************************# 
class Inputs:
    def __init__(self, tiempo, maximum):
        self.amplitude = 0
        self. tiempo = tiempo
        self.cont= 0
        self.max = maximum

    def pwm_ramp_step(self):
        if self.amplitude <= self.max:
            self.amplitude +=1
        return self.amplitude

    def pwm_triangular(self):
        if self.cont < self.max:
            amplitude += 1
            self.cont +=1
        elif (self.cont == self.max):
            amplitude -= 1
        return amplitude
        
# Step Function
    def pwm_step_function(self):
        u = (self.tiempo >= 0)*self.amplitude
        return u


    def pwm_manual(self):
        if keyboard.read_key() == 'a' or keyboard.read_key() == 'A':
            self.contador += 5
            print('Valor del contador: ', contador, flush = True)
        elif keyboard.read_key() == 'd' or keyboard.read_key() == 'D':
            self.contador -= 5
            print('Valor del contador: ', contador, flush = True)       
        
