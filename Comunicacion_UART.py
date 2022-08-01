## Tecnológico de Costa Rica

### Autor: Jorge Andrés Brenes Alfaro

## Comunicación UART

#El código desarrollado a continuación permite la comunicación de una tajeta
#NVIDIA Jetson TX 2 con un PSoC con el fin de enviar datos para controlar
#una planta de péndulo amortiguado a hélice (PAHM).

import Jetson.GPIO
import serial
import time

pin_transmit = 8
pint_receive = 10
#pwm_value = randint(0,4)

#pin_transmit = serial.Serial('??', baudrate=115200, parity=serial.PARITY.NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
#pin_receive = serial.Serial('??', baudrate=115200, parity=serial.PARITY.NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_transmit, GPIO.OUT, initial=GPIO.HIGH)  # pin_transmit set as output
GPIO.setup(pin_receive, GPIO.IN, initial=GPIO.HIGH)   # pin_transmit set as output

#while True:
    #pwm_value = randint(0,4)
    #rx_data = pin_receive.read()
    #print(rx_data)
    #pwm_value = RL_controller(rx_data) # futuramente se llama al controlador de RL
    #pin_transmit.write(pwm_value)

try:
    while True:
        pwm_value = randint(0,4)
        print('PWM value is: ', pwm_value)
        print('***** Data Receiving from PSoC *****')
        rx_data = GPIO.input(pin_receive)
        print('Data value is: ', rx_data)
        time.sleep(1)
        print('***** Data Transmitting from Jetson *****')
        GPIO.output(pwm_value)
        time.sleep(1)
finally:
    GPIO.cleanup()


# $ /boot/config.txt
# $ enable_uart= 1
