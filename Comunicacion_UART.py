## Tecnológico de Costa Rica
### Autor: Jorge Andrés Brenes Alfaro
## Comunicación UART

# El código desarrollado a continuación permite la comunicación de una tajeta
# NVIDIA Jetson TX 2 con un PSoC con el fin de enviar datos para controlar
# una planta de péndulo amortiguado a hélice (PAHM).

import serial
import time


serial_port = serial.Serial('dev/ttyTHS2', baudrate=115200, parity=serial.PARITY.NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)#, timeout=1)

time.sleep(1)

serial_port.write('Demostración de UART')
cont=0
while True:
    if serial_port.inWaiting() > 0:
        datos = serial_port.read()
        print('Se recibe: ', datos)

        serial_port.write(datos)
        if datos == '/r'.encode():
            serial_port.write('/n'.encode())
        if cont == 20:
            print(exit)
            exit()
        cont += 1
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
