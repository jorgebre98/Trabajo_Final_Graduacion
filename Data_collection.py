from Data_Classes import *

# Definición del puerto serial
serial_port  = serial.Serial("/dev/ttyTH2", baudrate = 115200,
                             stopbits = serial.STOPBITS_ONE,
                             bytesize = serial.EIGHTBITS,
                             parity = serial.PARITY_NONE)

time.sleep(0.5) #Dar tiempo para asignación de pines

uart = TransmitReceive(serial_port)

print('************ Starting *************', flush=True)
uart.reset()
#uart.create_pwm()

rt = RepeatedTimer(0.02, uart.Transmit_Receive) # No need of rt.start()
try:
    time.sleep(10) # long running job

except KeyboardInterrupt:
    print("Exiting Program")
    uart.reset()
    serial_port.close()
    #uart.turn_off()

except Exception as exception_error:
    print("Error occurred.")
    print("Error: " + str(exception_error))
    uart.reset()
    serial_port.close()
    #uart.turn_off()

finally:
    rt.stop()
    uart.csv.doc()
    uart.reset()
    serial_port.close()
    pass
