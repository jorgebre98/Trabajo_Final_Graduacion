import time
import serial
import struct
import random
import xlsxwriter

def Transmit_and_Receive(ser, num): # Serial port and float number
        print("\n**Transmitting**")
        print('Number to transmit: ', num)
        packed = struct.pack('!f', num)# float packed into bytes. The '!' ensures that it's in network byte order (big-endian).
        integers = [c for c in packed] # Each character correspond a interger.
        binaries = [bin(i) for i in integers] # Convert to binary representation.
        stripped_binaries = [s.replace('0b', '') for s in binaries] # Strip off the '0b'.
        padded = [s.rjust(8, '0') for s in stripped_binaries] # Make sure all has 8 bits.
        binary =''.join(padded)
        print('Packed: %s' % repr(packed),'\nBinary: ', binary, flush=True)
        start = time.time()
        ser.write(packed)
        print('**Transmission Finished**',flush=True)
        print('\n**Receiving**',flush=True)
        data_receive = ser.read(4)
        latencia = time.time() - start
        data = struct.unpack('!f', data_receive) # Convert bytes to float
        print('Data Receive:',data_receive)
        print('Float Data Receive: ', data[0])
        return data[0], latencia

def archivo_excel(values):
    archive = xlsxwriter.Workbook("Data_collection.xlsx")
    hoja = archive.add_worksheet()
    names = ['Latencia','Entrada','Ángulo']
    for j in range(len(names)):
        hoja.write(0,j,names[j])
        
    for j in range(len(values)):
        for i in range(len(values[j])):
            hoja.write(j+1,i,values[j][i]) # row, col, data
    archive.close()


# Port definition
serial_port = serial.Serial("/dev/ttyTHS2",
                            baudrate=115200,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)

cont = 0
values = [[0,0,0]]

while cont != 200:
        pwm_value = round(random.uniform(0,4),4)
        data_receive, latencia = Transmit_and_Receive (serial_port, pwm_value)
        #print(type(data_receive)) Es una tupla
        values.append([latencia, pwm_value, data_receive])
        cont+=1

archivo_excel(values)
serial_port.close()




