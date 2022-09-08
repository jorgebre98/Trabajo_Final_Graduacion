import time
import serial
import struct
import random

# Port definition
serial_port = serial.Serial("/dev/ttyTHS2",baudrate=115200,stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)

# PRUEBA 1
serial_port.reset_input_buffer()
serial_port.reset_output_buffer()
try:
        while True:
                contador = 280#125+(random.randint(0,4)/4)*125 #int(input('PWM: '))
                if serial_port.inWaiting() > 0:
                        packed = struct.pack('!i',contador)
                        serial_port.write(packed)
                        receive = serial_port.read(4)
                        data = struct.unpack('!i',receive)
                        print('Dato Transmitido: {0} y Dato recibido: {1}'.format(contador,data[0]))

except KeyboardInterrupt:
        print("Exiting Program")

except Exception as exception_error:
        print("Error occurred.")
        print("Error: " + str(exception_error))

finally:
        serial_port.close()
        pass
