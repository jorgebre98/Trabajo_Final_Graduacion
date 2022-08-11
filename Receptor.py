import serial
import struct
import random

def binary(num):
    print('Transmitting: ',num)
    print('')
    packed = struct.pack('!f', num)
    print ('Characters: %s' % repr(packed))
    integers = [c for c in packed] # Se obtiene los enteros de los caracteres.
    binaries = [bin(i) for i in integers] # Se convierte cada entero a binario.
    stripped_binaries = [s.replace('0b', '') for s in binaries] # Se quita '0b' de cada binario.
    padded = [s.rjust(8, '0') for s in stripped_binaries] # Se ajusta el binario a 8 bits
    val = ''.join(padded)
    print('Binary to transmit: ',val)
    return val,packed
    
   
#serial_port = serial.Serial("/dev/ttyTHS2",baudrate=115200,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
serial_port = serial.Serial("/dev/ttyUSB0",baudrate=115200,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)


cont = 0
#serial_port.open()
while cont != 2:
	data = serial_port.read(size=4)
	data_2 = struct.unpack('!f', data)
	print('Data receive: ', data)
        print('Float Data Receive: ',data_2)
	val, data_t = binary(round(random.uniform(0,4),4))
	#data_2 = float(data_2)	
#	print(type(data_2))
	serial_port.write(data_t)
	cont += 1
