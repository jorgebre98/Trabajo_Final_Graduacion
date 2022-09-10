import keyboard

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
