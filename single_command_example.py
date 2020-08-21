import serial
port = 'COM4'  # You will need to change this

ser = serial.Serial(port=port, baudrate=921600, timeout=1)
### set voltage to 10 and read return

voltage = 20
print('Voltage sent: ' + str(voltage))

ser.write(('setVOLT' + str(voltage) + '\r').encode())
returned = ser.read_until('\r'.encode())
returnVoltage = int(returned[:-1]) #### remove '.\r' from the string and cast to int

print('Voltage returned: ' + str(returnVoltage))
print('Equal: ' + str(voltage == returnVoltage))