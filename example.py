import serial
import time
import math

port = 'COM7' # You will need to change this

# Update() is used to send update commands and check if they are applied
def Update(writeCommand, readCommand, expected):
    run = True
    timeout = 0
    while run:
        ser.write(writeCommand + '\r')
        ser.write(readCommand+'\r')
        returned = ser.read_until('\r')
        if (expected + '\r' == returned):
            print (writeCommand + ' Successful')
            run = False
        else:
            ser.flushInput()
            ser.flushOutput()
            timeout = timeout + 1 
            time.sleep(0.3)
            if (timeout > 10):
                print('Error updating' + writeCommand)        
                run = False
                ser.close()
                exit()
        time.sleep(0.1)

ser = serial.Serial(port=port, baudrate=9600, timeout=1)

#Ensure Amplifer is disabled
Update('DISABLE', 'isENABLE', 'FALSE')
# Parameters 
#Power limit = 50W
#Min Freq = 35 kHz
#Max Freq = 40 kHz
#Freq = 37 kHz
#Voltage = 20Vpp
#Parallel resonance tracking, phase ref = 0, control = 0.1

#Power Limit in mW
Update('setMAXLPOW50000', 'getMAXLPOW', '50000')

#Max Frequency in Hz
Update('setMAXFREQ40000', 'getMAXFREQ', '40000')

#Max Frequency in Hz
Update('setMINFREQ35000', 'getMINFREQ', '35000')

#Disable Phase tracking to allow frequency update
Update('disPHASE', 'isPHASE', 'FALSE')

#Frequency in Hz
Update('setFREQ37000', 'getFREQ', '37000')

#Volts in V
Update('setVOLT20', 'getVOLT', '20')

#Target Phase in Deg
Update('setPHASE0', 'getPHASE', '0')

#Phase control gain 1/1000 , negative to track parallel resonance
Update('setPHASEGAIN-100', 'getPHASEGAIN', '-100')

#Disable Current Tracking 
Update('disCURRENT', 'isCURRENT', 'FALSE')

#Disable Power Tracking 
Update('disPOWER', 'isPOWER', 'FALSE')

#ENABLE PHASE Tracking 
Update('enPHASE', 'isPHASE', 'TRUE')

#ENABLE 
Update('ENABLE', 'isENABLE', 'TRUE')

ramp = 0
while True:
    Update('setVOLT' + str(ramp), 'getVOLT', ''+ str(ramp))
    ramp = ramp + 1
    if ramp > 20:
         ramp = 0

Update('DISABLE', 'isENABLE', 'FALSE')
ser.close()