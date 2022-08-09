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


# ********************************** Step Function **********************************#
def step_function(A,t):
    u = (t >= 0)*A
    return u

# ********************************** Ramp Function **********************************#
def ramp_function(A,t):
    r = t*step_function(A,t)
    return r

# *********************** Function to create .xlsx archives *************************#
def archivo_excel(values):
    archive = xlsxwriter.Workbook("Data_collection.xlsx")
    hoja = archive.add_worksheet()
    names = ['Latencia','Entrada','Ángulo']
    for j in range(len(names)):
        hoja.write(0,j,names[j])

    for j in range(len(values)):
        for i in range(len(values[j])):
            hoja.write(j+1,i,values[j][i]) # row, col, data
    archive.close()


# ************************* Data Transmission and Reception *************************#

# Definicion del puerto
serial_port = serial.Serial("/dev/ttyTHS2", 
			baudrate=115200,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)

time.sleep(0.02)

serial_port.write('Demostracion de UART'.encode())
serial_port.write('\r\nNVIDIA Jetson TX2\r\n'.encode())


star, end, sampling = -2,10,0.02
tiempo = np.concatenate([np.arange(star,end,sampling), np.zeros(1000)])
Amplitude = round(random.uniform(0,4),4)
step = step_function(Amplitude,tiempo)
r = ramp_function(Amplitude,tiempo)
print('\r\nAmplitud: ',Amplitude,'\r\n')

values = [[0,0,0]]
cont = 0

#while True:
while cont <= 500:
        if serial_port.inWaiting() > 0:
                #pwm_value= str(round(random.uniform(0,4),10)).encode() # Entrada random
                pwm_value = step[cont] # Entrada escalón
                #pwm_value= r[cont] # Entrada rampa
                ini = time.time()
                serial_port.write(str(pwm_value).encode())
                angle = serial_port.read()
                fin = time.time()
                latencia = fin-ini
                values.append([latencia, pwm_value,angle])
                #print('Datos recibidos: ',float(angle))
                print("\r\nLatencia: ", latencia,"\r\nDatos recibidos: ", angle, "\r\nDatos tansmitidos: ", pwm_value)        
                cont += 1
archivo_excel(values)
print('\r\nValores: ', values)
serial_port.close()





