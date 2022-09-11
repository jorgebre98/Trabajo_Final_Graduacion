#   Copyright (C) 2022 Jorge Brenes Alfaro.
#   EL5617 Trabajo Final de Graduación.
#   Escuela de Ingeniería Electrónica.
#   Tecnológico de Costa Rica.

#   This file is responsible for getting data from the PAHM. To do this, this file makes use of
#   the TransmitReceive, Timer and Inputs classes, which are in their respective file.

import numpy as np
import matplotlib.pyplot as plt

from Timer import *
from  Inputs_Set import *
from Transmit_and_Receive import *

#   Port serial definition.
serial_port  = serial.Serial("/dev/ttyTHS2", baudrate = 115200,
                             stopbits = serial.STOPBITS_ONE,
                             bytesize = serial.EIGHTBITS,
                             parity = serial.PARITY_NONE)

time.sleep(0.5) #   Time for pin assignment

run_time = 30 #     Time for long running job
start, sampling, end = -2, 0.02, span/sampling #    Start time, sampling period and ent time
tiempo = np.arange(start, end, samplig)

PAHM = TransmitReceive(serial_port, tiempo)

print('************ Starting *************', flush=True)
PAHM.reset()
print('Data_Recolecting .....', flush=True)

rt = RepeatedTimer(0.02, uart.Transmit_Receive) # No need of rt.start()

try:
    time.sleep(30) # long running job

except KeyboardInterrupt:
    print("Exiting Program")
    PAHM.reset()
    PAHM.turn_off()

except Exception as exception_error:
    print("Error occurred.")
    print("Error: " + str(exception_error))
    PAHM.reset()
    PAHM.turn_off()
    
finally:
    rt.stop()
    PAHM.csv_doc()
    PAHM.turn_off()
    print('************ Finished *************', flush=True)
    pass
