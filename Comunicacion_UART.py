## Tecnológico de Costa Rica

### Autor: Jorge Andrés Brenes Alfaro

## Comunicación

#El código desarrollado a continuación permite la comunicación de una tajeta
#NVIDIA Jetson TX 2 con un PSoC con el fin de enviar datos para controlar
#una planta de péndulo amortiguado a hélice (PAHM).

import Jetson.GPIO
import time

GPIO.setmode(GPIO.BOARD)

pin_transmit = 8
pint_receive = 10
baudrate = 115200
pwm_value = randint(0,4)

while True:
    try:
        print('Data Transmitting from Jetson')
        pin_transmit.write(pwm_value.enconde())
        print('Data Receiving from PSoC')
        data = pin_receive.readline()
        if data:
            print(data)
            time.sleep(1)
    except Exception as e:
        print(e)
        pín_transmit.close()
