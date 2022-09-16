#   Copyright (C) 2022 Jorge Brenes Alfaro.
#   EL5617 Trabajo Final de Graduación.
#   Escuela de Ingeniería Electrónica.
#   Tecnológico de Costa Rica.

#   This file is responsible for getting data from the PAHM. To do this, this file makes use of
#   the TransmitReceive, Timer and Inputs classes, which are in their respective file.

import argparse
import numpy as np
import matplotlib.pyplot as plt


from Timer import *
from Transmit_and_Receive import *


parser = argparse.ArgumentParser(description='Coleccione datos de la planta.')
parser.add_argument('--input',type=str,default="",help='nombre de archivo de entrada')
parser.add_argument('--output',type=str,default="",help='nombre de archivo de salida')
args = parser.parse_args()

playbackMode = (args.input != "")
storeOutput  = (args.output != "")
#print("1: {0}, 2: {1}.".format(playbackMode,storeOutput))




#   Port serial definition.
serial_port  = serial.Serial("/dev/ttyTHS2", baudrate = 115200,
                             stopbits = serial.STOPBITS_ONE,
                             bytesize = serial.EIGHTBITS,
                             parity = serial.PARITY_NONE)

time.sleep(0.5) #   Time for pin assignment

PAHM = TransmitReceive(serial_port)

if playbackMode:
    with open(args.input, newline='') as file_name:
        array=np.loadtxt(file_name, delimiter=",")
        PAHM.pwm_set_safe_value(array[:,1])
else:
    PAHM.pwm_set_safe_value(0.0)




print('************ Starting *************\n', flush=True)
PAHM.reset()
print('Data Colecting ...', flush=True)

rt = RepeatedTimer(0.02, PAHM.Transmit_Receive) # No need of rt.start()


def comando(valor):
    PAHM.pwm_set_safe_value(int(valor)/1000.0)

try:
    #PLAYBACK
    
    if playbackMode:
          time.sleep(len(PAHM.pwm)*0.02)
    else:
        master = tkinter.Tk()
        master.title('My PWM value')
        master.geometry('500x100') 
        w = tkinter.Scale(master, from_=0, to=1000, orient=tkinter.HORIZONTAL,length=800,command=comando,bg='white', fg='black', width=20)
        w.pack()
        tkinter.mainloop()
        
        print("Exiting Program...")

        
    if storeOutput:
       PAHM.csv_doc(args.output)


except KeyboardInterrupt:
    print("Exiting Program...")
    PAHM.reset()
    PAHM.turn_off()

except Exception as exception_error:
    print("Error occurred.")
    print("Error: " + str(exception_error))
    PAHM.reset()
    PAHM.turn_off()
    
finally:
    rt.stop()
    PAHM.turn_off()
    
    #plt.subplot(1,2,1)
    #plt.plot(PAHM.values[:,1])
    #plt.subplot(1,2,2)
    #plt.plot(PAHM.values[:,2])
    #plt.show()
    print('************ Finished *************', flush=True)
    pass
