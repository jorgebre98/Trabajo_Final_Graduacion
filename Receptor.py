import serial
import struct
import random

def binary(num):
    print('Transmitting: ',num)
    packed = struct.pack('!f', num)
    print ('Caracteres: %s' % repr(packed))
    
    integers = [c for c in packed] # Se obtiene los enteros de los caracteres.
    print ('Enteros: %s' % integers)

    binaries = [bin(i) for i in integers] # Se convierte cada entero a binario.
    stripped_binaries = [s.replace('0b', '') for s in binaries] # Se quita '0b' de cada binario.
    padded = [s.rjust(8, '0') for s in stripped_binaries] # Se ajusta el binario a 8 bits
    print ('Binarios: %s' % padded)
    val = ''.join(padded)
    print('Valor binario a transmitir: ',val)
    return val,packed
    
   
serial_port = serial.Serial("/dev/ttyUSB0",baudrate=115200,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)

cont = 0
#serial_port.open()
while cont != 2:
	data = serial_port.read(size=4)
	data_2 = struct.unpack('!f', data)
	print(type(data_2))
	print('Dato recibido: ',data)


	val,data_t = binary(round(random.uniform(0,4),4))
	serial_port.write(data_t)
	cont += 1