import time
import serial
import struct
import random
import xlsxwriter

def Transmit_and_Receive(ser, num): # Serial port and float number
        print('Float number: ', num)
        # float packed into bytes. The '!' ensures that it's in network byte order (big-endian).
        packed = struct.pack('!f', num)
        integers = [c for c in packed] # Each character correspond a interger.
        binaries = [bin(i) for i in integers] # Convert to binary representation.
        stripped_binaries = [s.replace('0b', '') for s in binaries] # Strip off the '0b'.
        padded = [s.rjust(8, '0') for s in stripped_binaries] # Make sure all has 8 bits.
        binary =''.join(padded)
        print('Characters: %s' % repr(packed), '\Intergers: %s' % intergers, '\nBinary to transmit: ', binary, flush=True)

        print("\r\n**Transmitting**\r\n")
        start = time.time()
        for b in packed:
                ser.write(b)
        print('**Transmission Finished**')
        
        print('**Receiving**')
        data_receive = ser.read(4)
        latencia = time.time() - start
        data = data.unpack('!f', data) # Convert bytes to float
        print('Data Receive: ', data)
        return data_receive, latencia

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
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE)

serial_port.open()
cont = 0

while cont <= 20:
        pwm_value = 3.2
        #value = random.uniform(0,4)
        data_receive, latencia = Transmit_and_Receive (serial_port, pwm_value)
        values = [[latencia, pwm_value, data_receive]]
        archivo_excel(values)
ser.close()