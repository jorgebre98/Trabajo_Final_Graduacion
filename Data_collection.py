## Tecnológico de Costa Rica
### Autor: Jorge Andrés Brenes Alfaro
## Comunicación UART

# El código desarrollado a continuación permite la comunicación de una tajeta
# NVIDIA Jetson TX 2 con un PSoC con el fin de enviar datos para controlar
# una planta de péndulo amortiguado a hélice (PAHM).

import serial
import time
import random

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
serial_port.close()
