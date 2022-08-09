## Tecnológico de Costa Rica
### Autor: Jorge Andrés Brenes Alfaro
## Comunicación UART

# El código desarrollado a continuación permite la comunicación de una tajeta
# NVIDIA Jetson TX 2 con un PSoC con el fin de enviar datos para controlar
# una planta de péndulo amortiguado a hélice (PAHM).

import time
import serial
import random
import xlsxwriter
import numpy as np
import pandas as pd

# Definicion del puerto
serial_port = serial.Serial("/dev/ttyTHS2", 
			baudrate=115200,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS)

time.sleep(0.02)

serial_port.write('Demostracion de UART'.encode())
serial_port.write('\r\nNVIDIA Jetson TX2\r\n'.encode())

values = [[0,0,0]]
cont = 0

#while True:
while cont <= 1000:
	if serial_port.inWaiting() > 0:
        	pwm_value= str(round(random.uniform(0,4),10)).encode() # Entrada random
                #pwm_value = step[cont] # Entrada escalón
                #pwm_value= r[cont] # Entrada rampa
        	ini = time.time()
        	serial_port.write(str(pwm_value).encode())
        	angle = serial_port.read()
        	fin = time.time()
        	latencia = fin-ini
        	values = [latencia, pwm_value,angle]
        	#print('Datos recibidos: ',angle)
		#print("\r\nLatencia: ", latencia,"\r\nDatos recibidos: ", datos, "\r\nDatos tansmitidos: ", pwm_value)        
                cont += 1
archivo_excel(values)
serial_port.close()


#star, end, sampling = -2,10,0.02
#time = np.concatenate([np.arange(star,end,sampling), np.zeros(1000)])
#Amplitude = round(random.uniform(0,4),4)


# ********************************** Función Escalón **********************************#
# Función escalón
def step_function(A,t):
    u = (t >= 0)*A
    return u

# ********************************** Función Rampa**********************************#
# Función rampa
def ramp_function(A,t):
    r = t*step_function(A,t)
    return r

# ********************************** Función para generar archivo .xlsx **********************************#
def archivo_excel(values):
    archivo = xlsxwriter.Workbook("Data_collection.xlsx")
    hoja = archivo.add_worksheet()
    names = ['Latencia','Entrada','Ángulo']
    for j in range(len(names)):
        hoja.write(0,j,names[j])

    for j in range(len(values)):
        for i in range(len(values[j])):
            hoja.write(j+1,i,values[j][i]) # row, col, data
    archivo.close()

# **********************************  **********************************#
