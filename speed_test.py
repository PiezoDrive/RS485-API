import serial
import time
import math
import numpy as np
from matplotlib import pyplot as plt

port = 'COM4' # You will need to change this

############################################################################
#                         RS485 RX speedTest                               #        
############################################################################


ser = serial.Serial(port=port, baudrate=921600, timeout=1)

# Disable amplifer and disable error reporting
ser.write('DISABLE\r'.encode())
ser.read_until('\r'.encode())
ser.write('disERROR\r'.encode())
ser.read_until('\r'.encode())

oldTime = time.time()
printFrame = 0
while True:
    ser.write('getSTATEWAVE\r'.encode())
    ser.read(2080)
    if (printFrame > 30):
        printFrame = 0
        print ('bps: ' + str((2080*8)/((time.time() - oldTime)/30)))
        oldTime = time.time()
    printFrame += 1