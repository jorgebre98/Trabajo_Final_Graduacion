#   Copyright (C) 2022 Jorge Brenes Alfaro.
#   EL5617 Trabajo Final de Graduación.
#   Escuela de Ingeniería Electrónica.
#   Tecnológico de Costa Rica.

#   This file is responsible for getting data from the PAHM. To do this, this file makes use of
#   the TransmitReceive, Timer and Inputs classes, which are in their respective file.

import sys
import numpy as np
import matplotlib.pyplot as plt

from Timer import *
from Transmit_and_Receive import *

#   Port serial definition.
serial_port  = serial.Serial("/dev/ttyTHS2", baudrate = 115200,
                             stopbits = serial.STOPBITS_ONE,
                             bytesize = serial.EIGHTBITS,
                             parity = serial.PARITY_NONE)

time.sleep(0.5) #   Time for pin assignment

PAHM = TransmitReceive(serial_port)

print('************ Starting *************\n', flush=True)
PAHM.reset()
print('Data Colecting ...', flush=True)

rt = RepeatedTimer(0.02, PAHM.Transmit_Receive) # No need of rt.start()

try:
    #PLAYBACK
    with open('step.csv', newline='') as file_name:
        array = np.loadtxt(file_name, delimiter=",")
    pwm_val = array[:,1]*1000+1000
    for i in pwm_val:
        PAHM.pwm(i)
    
    if len(sys.argv) > 1:
        PAHM.csv_doc(sys.argv[1])

#def comando(valor):
#    PAHM.pwm_setvalue(valor)

#try:
#    master = tkinter.Tk()
#    master.title('My PWM value')
#    master.geometry('500x100') 
#    w = tkinter.Scale(master, from_=1000, to=1300, orient=tkinter.HORIZONTAL,length=400,command=comando,bg='white', fg='black', width=20)
#    w.pack()
#    tkinter.mainloop()
    
#    print("Exiting Program...")

    
#    if len(sys.argv) > 1:
#        PAHM.csv_doc(sys.argv[1])


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
    
    plt.subplot(1,2,1)
    plt.plot(PAHM.values[:,1])
    plt.subplot(1,2,2)
    plt.plot(PAHM.values[:,2])
            
    plt.show()
    print('************ Finished *************', flush=True)
    pass
