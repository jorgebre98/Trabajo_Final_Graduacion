## Tecnológico de Costa Rica
### Autor: Jorge Andrés Brenes Alfaro
## Comunicación UART

# El código desarrollado a continuación permite la comunicación de una tajeta
# NVIDIA Jetson TX 2 con un PSoC con el fin de enviar datos para controlar
# una planta de péndulo amortiguado a hélice (PAHM).

import time
import serial
import random
import numpy as np
import matplotlib.pyplot as plt


# Definici[on del puerto
serial_port = serial.Serial("/dev/ttyTHS2", 
			baudrate=115200,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS)

time.sleep(0.002)

serial_port.write('Demostracion de UART'.encode())
serial_port.write('\r\nNVIDIA Jetson TX2\r\n'.encode())

cont = 0
initial_value = int(input("Valor inicial del PWM (0-4): "))

while cont < 20:
    if serial_port.inWaiting() > 0:
        serial_port.write(initial_value)
        datos = serial_port.read()
        print("Datos recibidos: ", datos)
        pwm_value = round(random.uniform(0,4))
        serial_port.write(pwm_value)
        print("Datos enviados: ", pwm_value)
        cont += 1 
serial_port.close()


star, end, sampling = -2,10,0.02
time = np.concatenate([np.arange(star,end,sampling), np.zeros(1000)])
Amplitude = round(random.uniform(0,4),4)

# Función escalón
def step_function(A,t):
    u = (t >= 0)*A
    return u

# Función rampa
def ramp_function(A,t):
    r = t*step_function(A,t)
    return r
