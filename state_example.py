import serial
import time
import math
import numpy as np
from matplotlib import pyplot as plt
from struct import *

port = 'COM3'  # You will need to change this

############################################################################
#                            Get State Example                            #
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
        

ser = serial.Serial(port=port, baudrate=921600, timeout=1)
#### Disable Error reporting, monitor amplifier state
ser.write('disERROR\r'.encode())
ser.read_until('\r'.encode())
while True:
    # Get state
    ser.write('getSTATE\r'.encode())
    returned = ser.read(80) #getSTATE with no waveform is 80 bytes long
    ser.flush()
    # Get amplifer state from returned buffer
    amp = AmpliferState(returned)
    print ('Enabled: ' + str(amp.enabled))
    print ('Phase Tracking: ' + str(amp.phaseTracking))
    print ('Power Tracking: ' + str(amp.powerTracking))
    print ('Current Tracking: ' + str(amp.currentTracking))
    print ('Amplifier Overload: ' + str(amp.errorAmp))
    print ('Load Overload: ' + str(amp.errorLoad))
    print ('Temperature Overload: ' + str(amp.errorTemperature))
    print ('Voltage: ' + str(amp.voltage))
    print ('Frequency: ' + str(amp.frequency))
    print ('Max Frequency: ' + str(amp.maxFrequency))
    print ('Min Frequency: ' + str(amp.minFrequency))
    print ('Phase Setpoint: ' + str(amp.phaseSetpoint))
    print ('Phase Control Gain: ' + str(amp.phaseControlGain))
    print ('Current Setpoint: ' + str(amp.currentSetpoint))
    print ('Current Control Gain: ' + str(amp.currentControlGain))
    print ('Power Setpoint: ' + str(amp.powerSetpoint))
    print ('Power Control Gain: ' + str(amp.powerControlGain))
    print ('Max Load Power: ' + str(amp.maxLoadPower))
    print ('Load Power: ' + str(amp.loadPower))
    print ('Amp Power: ' + str(amp.ampliferPower))
    print ('Phase Measured: ' + str(amp.measuredPhase))
    print ('Current Measured: ' + str(amp.measuredCurrent))
    print ('Impedance: ' + str(amp.Impedance))
    print ('Temperature: ' + str(amp.temperature))
    print ('Transformer Turns ' + str(amp.transformerTruns))
    #### Monitor for errors
    if amp.errorLoad:
        print('Load Overload')
        exit()
    if amp.errorAmp:
        print('Amplifier Overload')
        exit()
    if amp.errorTemperature:
        print('Temperature Overload')
        exit()

    print('\n\r')

    time.sleep(0.5)



