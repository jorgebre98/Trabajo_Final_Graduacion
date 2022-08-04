## Tecnológico de Costa Rica
### Autor: Jorge Andrés Brenes Alfaro
## Comunicación UART

# El código desarrollado a continuación permite la comunicación de una tajeta
# NVIDIA Jetson TX 2 con un PSoC con el fin de enviar datos para controlar
# una planta de péndulo amortiguado a hélice (PAHM).

import serial
import time


serial_port = serial.Serial("/dev/ttyTHS2", 
			baudrate=115200,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS)

time.sleep(1)

serial_port.write('Demostracion de UART'.encode())
serial_port.write('\r\nNVIDIA Jetson TX2\r\n'.encode())

while True:
    if serial_port.inWaiting() > 0:
        datos = serial_port.read()
        print(datos)
        serial_port.write(str(datos).encode())
        if datos == "\r".encode():
            serial_port.write("\n".encode())
serial_port.close()


#GPIO.setmode(GPIO.BOARD) GPIO.setwarnings(False)
#GPIO.setup(pin_transmit, GPIO.OUT, initial=GPIO.HIGH)  # pin_transmit
#set as output GPIO.setup(pin_receive, GPIO.IN, initial=GPIO.HIGH)  #
#pin_transmit set as output

#while True:
    #pwm_value = randint(0,4)
    #rx_data = pin_receive.read()
    #print(rx_data)
    #pwm_value = RL_controller(rx_data) # futuramente se llama al controlador de RL
    #pin_transmit.write(pwm_value)

#try:
#    while True:
        #pwm_value = randint(0,4)
        #print('PWM value is: ', pwm_value)
        #print('***** Data Receiving from PSoC *****')
        #rx_data = GPIO.input(pin_receive)
        #print('Data value is: ', rx_data)
        #time.sleep(1)
        #print('***** Data Transmitting from Jetson *****')
        #GPIO.output(pwm_value)
        #time.sleep(1)
#finally:
    #GPIO.cleanup()


# $ /boot/config.txt
# $ enable_uart= 1
