import serial
import struct

ser = serial.Serial("/dev/ttyTHS2", 
			baudrate=115200,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)

value = 3.2
bina = struct.pack('!f',value)  # The "!" ensures that it's in network byte order (big endian)
print('Binario: ',bina)

for b in bina:
	print('Transmitting: ',b)
	ser.write(b)

print('**Transmission Finished**')
print('**Receiving**')
data = ser.read(4)
data = struct.unpack('!f', data)
print(data)
ser.close()
