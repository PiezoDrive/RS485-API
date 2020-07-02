import serial
import time
import math
import numpy as np
from matplotlib import pyplot as plt

port = 'COM3' # You will need to change this

############################################################################
#                 Impdance Sweeper and RS485 benchmark                     #        
############################################################################


# Update() is used to send update commands and check if they are applied
def Update(writeCommand, readCommand, expected):
    run = True
    timeout = 0
    while run:
        #note added encode required for pySerial for python3
        ser.write((writeCommand + '\r').encode()) 
        ser.write((readCommand+'\r').encode())
        returned = ser.read_until('\r')
        returned = str(returned)[2:-3]
        if (expected == returned):
            #print (writeCommand + ' Successful Timeout ' + str(timeout))
            run = False

        else:
            ser.flushInput()
            ser.flushOutput()
            timeout = timeout + 1 
            
            if (timeout > 100):
                print('Error updating' + writeCommand)        
                run = False
                ser.close()
                exit()

def Measurement(readCommand):
    run = True
    timeout = 0
    while run:
        ser.write((readCommand+'\r').encode())
        returned = ser.read_until('\r')
        returned = str(returned)[2:-3]
        try:
            #print (writeCommand + ' Successful Timeout ' + str(timeout))
            returnedFloat = float(returned)
            run = False
        except:
            ser.flushInput()
            ser.flushOutput()
            timeout = timeout + 1 
            
            if (timeout > 100):
                print('Error Reading')      
                run = False
                ser.close()
                exit()



    return returnedFloat

ser = serial.Serial(port=port, baudrate=9600, timeout=0.04)

#Ensure Amplifer is disabled
Update('DISABLE', 'isENABLE', 'FALSE')
#Sweep Parameters 
#Start Frequency = 35 kHz
#End Frequency = 100 kHz
#Voltage = 5 Vpp
#Frequency Steep = 100 Hz 

start_frequency = 35000
end_frequency = 100000
frequency_step = 100

#Disable all tracking
Update('disPHASE', 'isPHASE', 'FALSE')
Update('disPOWER', 'isPOWER', 'FALSE')
Update('disCURRENT', 'isCURRENT', 'FALSE')

#Set min and max
Update('setMAXFREQ' + str(end_frequency), 'getMAXFREQ', str(end_frequency))
Update('setMINFREQ' + str(start_frequency), 'getMINFREQ', str(start_frequency))

#Set volt
Update('setVOLT5', 'getVOLT', '5');
Update('ENABLE', 'isENABLE', 'TRUE');

#Make frequency array

frequency_array = np.arange(start_frequency, end_frequency, frequency_step)
impdance_array = []

t = time.time()
timeSum = 0
for frequency in frequency_array:
    Update('setFREQ' + str(frequency), 'getFREQ', str(frequency))
    impdance = Measurement('readIMP')
    impdance_array.append(impdance)
    timeSum += time.time() - t
    t = time.time()
    print('Frequency: ' + str(frequency) + ' Impdance: ' + str(impdance))

print('\n')
print('Complete, average measurements a second: ' + str(1.0/(timeSum/len(frequency_array))))
print('Complete, average commands a second: ' + str(3.0/(timeSum/len(frequency_array))))
print('Complete, average bps: ' + str(8*10*(3.0/(timeSum/len(frequency_array)))))
ser.close()

plt.plot(frequency_array, impdance_array)
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Impdance (Ohms)')
plt.show()