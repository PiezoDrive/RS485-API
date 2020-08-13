import serial
import time
import math
import numpy as np
from matplotlib import pyplot as plt
from struct import *


port = 'COM4'  # You will need to change this

############################################################################
#                           Frequency Sweep Example                        #
############################################################################

###### Define amplifier class to unpack data buffer
class AmpliferState:
    def __init__(self, data):
        self.enabled = bool(data[0])
        self.phaseTracking = bool(data[1])
        self.currentTracking = bool(data[2])
        self.powerTracking = bool(data[3])
        self.errorAmp = bool(data[4])
        self.errorLoad = bool(data[5])
        self.errorTemperature = bool(data[6]) 
        self.voltage = float(unpack('f', data[8:12])[0])
        self.frequency = float(unpack('f', data[12:16])[0]) 
        self.minFrequency = float(unpack('f', data[16:20])[0]) 
        self.maxFrequency = float(unpack('f', data[20:24])[0])
        self.phaseSetpoint = float(unpack('f', data[24:28])[0])
        self.phaseControlGain = float(unpack('f', data[28:32])[0])
        self.currentSetpoint = float(unpack('f', data[32:36])[0])
        self.currentControlGain = float(unpack('f', data[36:40])[0]) 
        self.powerSetpoint = float(unpack('f', data[40:44])[0])
        self.powerControlGain = float(unpack('f', data[44:48])[0])
        self.maxLoadPower = float(unpack('f', data[48:52])[0])
        self.ampliferPower = float(unpack('f', data[52:56])[0])
        self.loadPower = float(unpack('f', data[56:60])[0])
        self.temperature = float(unpack('f', data[60:64])[0])
        self.measuredPhase = float(unpack('f', data[64:68])[0])
        self.measuredCurrent = float(unpack('f', data[68:72])[0])
        self.Impedance = float(unpack('f', data[72:76])[0])
        self.transformerTruns = float(unpack('f', data[76:80])[0])

# Define update function to make code cleaner        
def update(command, value):
    ser.write((command + value + '\r').encode())
    ser.read_until('\r'.encode())

# Define get amplifer state function to make code cleaner
# returns an amplifer object
def getAmplifierState():
    ser.write('getSTATE\r'.encode())
    returned = ser.read(80)
    ser.flushInput()
    amplifer = AmpliferState(returned)
    return amplifer

# Setup serial connection
ser = serial.Serial(port=port, baudrate=921600, timeout=1)
# Disable amplifer while sweep parametes are set
update('DISABLE', '')
# Disable error reports, will monitor errors from amplifier state
update('disERROR', '')

#Sweep Parameters 
#Start Frequency = 35 kHz
#End Frequency = 100 kHz
#Voltage = 5 Vpp
#Frequency Steep = 100 Hz 

start_frequency = 35000
end_frequency = 100000
frequency_step = 100

update('disPHASE', '')
update('disPOWER', '')
update('disCURRENT', '')

#Set min and max
update('setMAXFREQ', str(end_frequency))
update('setMINFREQ', str(start_frequency))

#Set volt
update('setVOLT', '5');
update('ENABLE', '');

# Build an array of frequency values
frequency_array = np.arange(start_frequency, end_frequency, frequency_step)
impdance_array = []

t = time.time()
timeSum = 0

# Preform sweep
for frequency in frequency_array:
    update('setFREQ', str(frequency))
    ampliferState = getAmplifierState()
    # Monitor for errors
    if ampliferState.errorAmp:
        print('Amplifer Overload')
        exit()
    if ampliferState.errorLoad:
        print('Load Overload')
        exit()
    if ampliferState.errorTemperature:
        print('Temperature Overload')
        exit()
    impdance = ampliferState.Impedance
    impdance_array.append(impdance)
    timeSum += time.time() - t
    t = time.time()
    print('Frequency: ' + str(frequency) + ' Impdance: ' + str(impdance))

# Disable output
update('DISABLE', '')
print('\n')
print('Complete, average measurements a second: ' + str(1.0/(timeSum/len(frequency_array))))
ser.close()

# Plot results
plt.plot(frequency_array, impdance_array)
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Impdance (Ohms)')
plt.show()