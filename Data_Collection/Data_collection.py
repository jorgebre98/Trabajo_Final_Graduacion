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

print('************ Starting *************', flush=True)
PAHM.reset()
print('Data_Recolecting ...', flush=True)

rt = RepeatedTimer(0.02, PAHM.Transmit_Receive) # No need of rt.start()

#try:
#    time.sleep(5) # long running job

def comando(valor):
    PAHM.pwm_setvalue(valor)

try:
    master = tkinter.Tk()
    w = tkinter.Scale(master, from_=950, to=2000, orient=tkinter.HORIZONTAL,length=400,command=comando)
    w.pack()
    tkinter.mainloop()
    print("Exiting Program...")

    PAHM.turn_off()
    
    if len(sys.argv) > 1:
        PAHM.csv_doc(sys.argv[1])

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
    print('************ Finished *************', flush=True)
    pass
