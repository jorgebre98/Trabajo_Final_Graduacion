## Tecnológico de Costa Rica
### Autor: Jorge Andrés Brenes Alfaro
## Archivo principal

# El código desarrollado a continuación permite el control de una planta de péndulo
# amortiguado a hélice (PAHM) mediante una tajeta NVIDIA Jetson TX 2.


# Bibliotecas.
import serial
import time

# Definición de puertos.
# El uso de UART1 utiliza /dev/ttyTHS2
# pines: GND = 1 / TX = 4 / RX = 5
serial_port = serial.Serial("/dev/ttyTYHS2",
                            baudrate = 115200,
                            stopbits = serial.STOPBITS_ONE,
                            bytesize = serial.EIGHTBITS
                            )

time.sleep(0.002)
angle_ref =  # Definición del ángulo de referencia

while True:
    if serial_port.inWaiting() > 0:
        angle = serial_port.read()
        print ("Angle receive: ", angle)
        pwm_value = RL_controller(angle, angle_ref)
        print("Valor del PWM: ", pwm_value)
        serial_port.write(pwm_value)
serial_port.close()


