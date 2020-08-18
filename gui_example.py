import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel, QSpinBox, QDoubleSpinBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import serial
from struct import *
import numpy as np

port = 'COM4'  # You will need to change this

############################################################################
#                        GUI Example, uses PyQt framework                  #
#                            See state example first                       #
############################################################################

###### Define amplifier class to unpack data buffer, includes waveforms
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
        self.voltageWave = []
        for i in range(0,250):
            self.voltageWave.append(float(unpack('f',data[80+(i*4):84+(i*4)])[0]))
        self.currentWave = []
        for i in range(250,500):
            self.currentWave.append(float(unpack('f',data[80+(i*4):84+(i*4)])[0]))
        self.voltage = self.voltage*self.transformerTruns

class App(QDialog):

    def __init__(self, argv):
        super().__init__()
        self.title = 'PDus210 - RS485 Example'
        self.left = 100
        self.top = 100
        self.width = 1800
        self.height = 800
        self.commands = []
        self.initUI()
        self.time = np.linspace(0, 47.8, 250) #Time array for waveform
        self.ser = serial.Serial(port=port, baudrate=921600, timeout=2) #Setup serial
        self.frequency = [0]
        self.phase = [0]
        self.time2 = [0]
        self.numberOfSamples = 1000
        self.reconnect = True
        print(argv)
        
    def initUI(self): #Setup GUI
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()
        self.updateViews()
        self.p1.vb.sigResized.connect(self.updateViews)

        #start timer for getState
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.getState)
        self.timer.start()
       
    def getState(self): #Update GUI with new amplifer state 
        if self.reconnect:
            self.reconnect = False
            # Disable error reports, will monitor errors from amplifier state
            self.addCommand('disERROR', '')
        error = False
        # Send commands in command list
        if(len(self.commands)>0):
            try:
                for command in self.commands:
                    self.ser.write((command + '\r').encode())
                    returned = self.ser.read_until('\r'.encode())
                    self.ser.flushInput()
                self.commands = []
            except:
                print('ERROR')
                error = True
                self.reconnect = True
                self.errorValue.setText('Communication')
                self.ser.flushInput()
        try: #Update amplifer state and GUI
            self.ser.write('getSTATEWAVE\r'.encode())
            returned = self.ser.read(2080)
            self.ser.flushInput()
            self.amp = AmpliferState(returned)
            self.enableValue.setText(str(self.amp.enabled))
            self.trackingValue.setText(str(self.amp.phaseTracking))
            self.currentTrackingValue.setText(str(self.amp.currentTracking))
            self.powerTrackingValue.setText(str(self.amp.powerTracking))
            self.voltageValue.setText(str(int(self.amp.voltage)) + ' V')
            self.frequencyValue.setText(str(int(self.amp.frequency)) + ' Hz')
            self.frequencyMaxValue.setText(str(int(self.amp.maxFrequency)) + ' Hz')
            self.frequencyMinValue.setText(str(int(self.amp.minFrequency)) + ' Hz')
            self.phaseValue.setText(str(int(self.amp.phaseSetpoint)) + ' Deg')
            self.phaseGainValue.setText(str(round(self.amp.phaseControlGain, 3)))
            self.currentValue.setText(str(round(self.amp.currentSetpoint/1000, 3)) + ' A')
            self.currentGainValue.setText(str(round(self.amp.currentControlGain, 3)))
            self.powerValue.setText(str(round(self.amp.powerSetpoint, 3)) + ' W')
            self.powerGainValue.setText(str(round(self.amp.powerControlGain, 3)))
            self.maxLoadPowerValue.setText(str(round(self.amp.maxLoadPower, 3)) + ' W')
            self.loadPowerValue.setText(str(round(self.amp.loadPower, 1)) + ' W')
            self.ampPowerValue.setText(str(round(self.amp.ampliferPower, 1)) + ' W')
            self.tempValue.setText(str(round(self.amp.temperature, 1)) + ' C')
            self.impValue.setText(str(round(self.amp.Impedance, 0)) + ' Ohms')

            ######### Update frequency and phase plots
            if(len(self.phase)==1):
                self.phase[0] = self.amp.measuredPhase
            self.phase = [self.amp.measuredPhase] + self.phase
            if (len(self.phase)>self.numberOfSamples):
                del self.phase[-1]

            if(len(self.frequency)==1):
                self.frequency[0] = self.amp.frequency
            self.frequency = [self.amp.frequency] + self.frequency
            if (len(self.frequency)>self.numberOfSamples):
                del self.frequency[-1]

            if (len(self.time2) < self.numberOfSamples):
                self.time2 = self.time2 + [0.05 + self.time2[-1]] 
            self.updateWaveform()

            #### Monitor for errors 
            if self.amp.errorLoad:
                error = True
                self.errorValue.setText('Load Overload')

            if self.amp.errorAmp:
                error = True
                self.errorValue.setText('Amplifer Overload')
            
            if self.amp.errorTemperature:
                error = True
                self.errorValue.setText('Temperature Overload')

        except Exception as e:
            print(e)
            error = True
            self.reconnect = True
            self.errorValue.setText('Communication')
            self.ser.flushInput()

        if not error:
            self.errorValue.setText('None')


    def addCommand(self, command, value): #Function to add commands to comand list
        if (value == ''):
            self.commands.append(command)
        else:
            self.commands.append(command+str(int(value)))
        
    def updateWaveform(self): #Updates graphs
        self.p1.clear()
        self.p1.plot(self.time, self.amp.voltageWave)
        self.p2.clear()
        self.p2.addItem(pg.PlotCurveItem(self.time, self.amp.currentWave, pen='b'))
        self.p2.setGeometry(self.p1.vb.sceneBoundingRect())
        self.p2.linkedViewChanged(self.p1.vb, self.p2.XAxis)   

        self.p1g.clear()
        self.p1g.plot(self.time2, self.phase)
        self.p2g.clear()
        self.p2g.addItem(pg.PlotCurveItem(self.time2, self.frequency, pen='b'))
        self.p2g.setGeometry(self.p1g.vb.sceneBoundingRect())
        self.p2g.linkedViewChanged(self.p1g.vb, self.p2g.XAxis) 
    
    def createGridLayout(self): #Build GUI
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()

        #WaveformGraph
        self.graphWidgetWaveform = pg.PlotWidget()
        self.p1 = self.graphWidgetWaveform.plotItem
        self.p1.setLabels(left = 'Voltage') 
        voltage = [0]
        time = [0]
        self.p1.plot(voltage, time)
        
        self.p2 = pg.ViewBox()
        self.p1.showAxis('right')
        self.p1.scene().addItem(self.p2)
        self.p1.getAxis('right').linkToView(self.p2)
        self.p2.setXLink(self.p1)
        self.p1.getAxis('right').setLabel('Current',color='#0000ff')
        self.p2line = self.p2.addItem(pg.PlotCurveItem([10,20,40,80,40,20], pen='b'))
        self.graphWidgetWaveform.setBackground('w')
        layout.addWidget(self.graphWidgetWaveform, 0,4,12,100)
        
        #Frequency and phase plot
        self.graphWidgetGraph = pg.PlotWidget()
        self.p1g = self.graphWidgetGraph.plotItem
        self.p1g.setLabels(left = 'Phase') 
        phase = [0]
        time = [0]
        self.p1g.plot(voltage, time)
        self.p2g = pg.ViewBox()
        self.p1g.showAxis('right')
        self.p1g.scene().addItem(self.p2g)
        self.p1g.getAxis('right').linkToView(self.p2g)
        self.p2g.setXLink(self.p1g)
        self.p1g.getAxis('right').setLabel('Frequency',color='#0000ff')
        self.p2lineg = self.p2g.addItem(pg.PlotCurveItem([0], pen='b'))
        self.graphWidgetGraph.setBackground('w')
        layout.addWidget(self.graphWidgetGraph, 12,4,12,100)

       #Enable
        #Define widgets
        self.enableLabel = QLabel('Enabled:')
        self.enableValue = QLabel('')
        self.enableEnableButton = QPushButton('Enable')
        self.disableEnableButton = QPushButton('Disable')
        self.enableEnableButton.clicked.connect(lambda:self.addCommand('ENABLE', ''))
        self.disableEnableButton.clicked.connect(lambda:self.addCommand('DISABLE', ''))
        #Add widgets to grid
        layout.addWidget(self.enableLabel, 0,0)
        layout.addWidget(self.enableValue, 0,1)
        layout.addWidget(self.enableEnableButton, 0,2)
        layout.addWidget(self.disableEnableButton, 0,3)

        #Phase Tracking
        #Define widgets
        self.trackingLabel = QLabel('Phase Tracking:')
        self.trackingValue = QLabel('')
        self.enableTrackingButton = QPushButton('Enable')
        self.disableTrackingButton = QPushButton('Disable')
        self.enableTrackingButton.clicked.connect(lambda:self.addCommand('enPHASE', ''))
        self.disableTrackingButton.clicked.connect(lambda:self.addCommand('disPHASE', ''))
        #Add widgets to grid
        layout.addWidget(self.trackingLabel, 1,0)
        layout.addWidget(self.trackingValue, 1,1)
        layout.addWidget(self.enableTrackingButton, 1,2)
        layout.addWidget(self.disableTrackingButton, 1,3)
       
        #Current Tracking
        #Define widgets
        self.currentTrackingLabel = QLabel('Current Tracking:')
        self.currentTrackingValue = QLabel('')
        self.enableCurrentTrackingButton = QPushButton('Enable')
        self.disableCurrentTrackingButton = QPushButton('Disable')
        self.enableCurrentTrackingButton.clicked.connect(lambda:self.addCommand('enCURRENT', ''))
        self.disableCurrentTrackingButton.clicked.connect(lambda:self.addCommand('disCURRENT', ''))
        #Add widgets to grid
        layout.addWidget(self.currentTrackingLabel, 2,0)
        layout.addWidget(self.currentTrackingValue, 2,1)
        layout.addWidget(self.enableCurrentTrackingButton, 2,2)
        layout.addWidget(self.disableCurrentTrackingButton, 2,3)

        #Power Tracking
        #Define widgets
        self.powerTrackingLabel = QLabel('Power Tracking:')
        self.powerTrackingValue = QLabel('')
        self.enablePowerTrackingButton = QPushButton('Enable')
        self.disablePowerTrackingButton = QPushButton('Disable')
        self.enablePowerTrackingButton.clicked.connect(lambda:self.addCommand('enPOWER', ''))
        self.disablePowerTrackingButton.clicked.connect(lambda:self.addCommand('disPOWER', ''))
        #Add widgets to grid
        layout.addWidget(self.powerTrackingLabel, 3,0)
        layout.addWidget(self.powerTrackingValue, 3,1)
        layout.addWidget(self.enablePowerTrackingButton, 3,2)
        layout.addWidget(self.disablePowerTrackingButton, 3,3)

        #Voltage
        #Define widgets
        self.voltageLabel = QLabel('Voltage:')
        self.voltageValue = QLabel('')
        self.voltageSpinner = QSpinBox()
        self.voltageSpinner.setMaximum(1000)
        self.voltageSpinner.setMinimum(0)
        self.voltageButton = QPushButton('Update')
        self.voltageButton.clicked.connect(lambda:self.addCommand('setVOLT', str(self.voltageSpinner.value())))
        #Add widgets to grid
        layout.addWidget(self.voltageLabel, 4,0)
        layout.addWidget(self.voltageValue, 4,1)
        layout.addWidget(self.voltageSpinner, 4,2)
        layout.addWidget(self.voltageButton, 4,3)

       #Frequency
        self.frequencyLabel = QLabel('Frequency:')
        self.frequencyValue = QLabel('')
        self.frequencySpinner = QSpinBox()
        self.frequencySpinner.setMaximum(520000)
        self.frequencySpinner.setMinimum(0)
        self.frequencyButton = QPushButton('Update')
        self.frequencyButton.clicked.connect(lambda:self.addCommand('setFREQ', str(self.frequencySpinner.value())))
        #Add widgets to grid
        layout.addWidget(self.frequencyLabel, 5,0)
        layout.addWidget(self.frequencyValue, 5,1)
        layout.addWidget(self.frequencySpinner, 5,2)
        layout.addWidget(self.frequencyButton, 5,3)
       #FrequencyMin
        self.frequencyMinLabel = QLabel('Min Frequency:')
        self.frequencyMinValue = QLabel('')
        self.frequencyMinSpinner = QSpinBox()
        self.frequencyMinSpinner.setMaximum(520000)
        self.frequencyMinSpinner.setMinimum(0)
        self.frequencyMinButton = QPushButton('Update')
        self.frequencyMinButton.clicked.connect(lambda:self.addCommand('setMINFREQ', str(self.frequencyMinSpinner.value())))
        #Add widgets to grid
        layout.addWidget(self.frequencyMinLabel, 6,0)
        layout.addWidget(self.frequencyMinValue, 6,1)
        layout.addWidget(self.frequencyMinSpinner, 6,2)
        layout.addWidget(self.frequencyMinButton, 6,3)
       #FrequencyMax
        self.frequencyMaxLabel = QLabel('Max Frequency:')
        self.frequencyMaxValue = QLabel('')
        self.frequencyMaxSpinner = QSpinBox()
        self.frequencyMaxSpinner.setMaximum(520000)
        self.frequencyMaxSpinner.setMinimum(0)
        self.frequencyMaxButton = QPushButton('Update')
        self.frequencyMaxButton.clicked.connect(lambda:self.addCommand('setMAXFREQ', str(self.frequencyMaxSpinner.value())))
        #Add widgets to grid
        layout.addWidget(self.frequencyMaxLabel, 7,0)
        layout.addWidget(self.frequencyMaxValue, 7,1)
        layout.addWidget(self.frequencyMaxSpinner, 7,2)
        layout.addWidget(self.frequencyMaxButton, 7,3)
       #Phase
        self.phaseLabel = QLabel('Phase Setpoint:')
        self.phaseValue = QLabel('')
        self.phaseSpinner = QSpinBox()
        self.phaseSpinner.setMaximum(180)
        self.phaseSpinner.setMinimum(-180)
        self.phaseButton = QPushButton('Update')
        self.phaseButton.clicked.connect(lambda:self.addCommand('setPHASE', str(self.phaseSpinner.value())))
        #Add widgets to grid
        layout.addWidget(self.phaseLabel, 8,0)
        layout.addWidget(self.phaseValue, 8,1)
        layout.addWidget(self.phaseSpinner, 8,2)
        layout.addWidget(self.phaseButton, 8,3)

        #Phase Gain setPHASEGAIN
        self.phaseGainLabel = QLabel('Phase Gain:')
        self.phaseGainValue = QLabel('')
        self.phaseGainSpinner = QDoubleSpinBox()
        self.phaseGainSpinner.setMaximum(100)
        self.phaseGainSpinner.setMinimum(-100)
        self.phaseGainButton = QPushButton('Update')
        self.phaseGainButton.clicked.connect(lambda:self.addCommand('setGAINPHASE', int(self.phaseGainSpinner.value()*1000)))
        #Add widgets to grid
        layout.addWidget(self.phaseGainLabel, 9,0)
        layout.addWidget(self.phaseGainValue, 9,1)
        layout.addWidget(self.phaseGainSpinner, 9,2)
        layout.addWidget(self.phaseGainButton, 9,3)

        #Current Setpoint
        self.currentLabel = QLabel('Current Setpoint:')
        self.currentValue = QLabel('')
        self.currentSpinner = QDoubleSpinBox()
        self.currentSpinner.setMaximum(20)
        self.currentSpinner.setMinimum(0)
        self.currentButton = QPushButton('Update')
        self.currentButton.clicked.connect(lambda:self.addCommand('setCURRENT', int(self.currentSpinner.value()*1000)))
        #Add widgets to grid
        layout.addWidget(self.currentLabel, 10,0)
        layout.addWidget(self.currentValue, 10,1)
        layout.addWidget(self.currentSpinner, 10,2)
        layout.addWidget(self.currentButton, 10,3)

        #Current Gain
        self.currentGainLabel = QLabel('Current Gain:')
        self.currentGainValue = QLabel('')
        self.currentGainSpinner = QDoubleSpinBox()
        self.currentGainSpinner.setMaximum(100)
        self.currentGainSpinner.setMinimum(0)
        self.currentGainButton = QPushButton('Update')
        self.currentGainButton.clicked.connect(lambda:self.addCommand('setGAINCURRENT', int(self.currentGainSpinner.value()*1000)))
        #Add widgets to grid
        layout.addWidget(self.currentGainLabel, 11,0)
        layout.addWidget(self.currentGainValue, 11,1)
        layout.addWidget(self.currentGainSpinner, 11,2)
        layout.addWidget(self.currentGainButton, 11,3)

        #Power Setpoint
        self.powerLabel = QLabel('Power Setpoint:')
        self.powerValue = QLabel('')
        self.powerSpinner = QDoubleSpinBox()
        self.powerSpinner.setMaximum(210)
        self.powerSpinner.setMinimum(0)
        self.powerButton = QPushButton('Update')
        self.powerButton.clicked.connect(lambda:self.addCommand('setTARPOW', int(self.powerSpinner.value()*1000)))
        #Add widgets to grid
        layout.addWidget(self.powerLabel, 12,0)
        layout.addWidget(self.powerValue, 12,1)
        layout.addWidget(self.powerSpinner, 12,2)
        layout.addWidget(self.powerButton, 12,3)

        #Power Gain
        self.powerGainLabel = QLabel('Power Gain:')
        self.powerGainValue = QLabel('')
        self.powerGainSpinner = QDoubleSpinBox()
        self.powerGainSpinner.setMaximum(100)
        self.powerGainSpinner.setMinimum(0)
        self.powerGainButton = QPushButton('Update')
        self.powerGainButton.clicked.connect(lambda:self.addCommand('setGAINPOWER', int(self.powerGainSpinner.value()*1000)))
        #Add widgets to grid
        layout.addWidget(self.powerGainLabel, 13,0)
        layout.addWidget(self.powerGainValue, 13,1)
        layout.addWidget(self.powerGainSpinner, 13,2)
        layout.addWidget(self.powerGainButton, 13,3)

        #Max load power
        self.maxLoadPowerLabel = QLabel('Max Load Power:')
        self.maxLoadPowerValue = QLabel('')
        self.maxLoadPowerSpinner = QDoubleSpinBox()
        self.maxLoadPowerSpinner.setMaximum(210)
        self.maxLoadPowerSpinner.setMinimum(0)
        self.maxLoadPowerButton = QPushButton('Update')
        self.maxLoadPowerButton.clicked.connect(lambda:self.addCommand('setMAXLPOW', int(self.maxLoadPowerSpinner.value()*1000)))
        #Add widgets to grid
        layout.addWidget(self.maxLoadPowerLabel, 14,0)
        layout.addWidget(self.maxLoadPowerValue, 14,1)
        layout.addWidget(self.maxLoadPowerSpinner, 14,2)
        layout.addWidget(self.maxLoadPowerButton, 14,3)

        #Power measurements
        self.ampPowerLabel = QLabel('Amp Power:')
        self.ampPowerValue = QLabel('')
        self.loadPowerLabel = QLabel('Load Power:')
        self.loadPowerValue = QLabel('')
        #Add widgets to grid
        layout.addWidget(self.ampPowerLabel, 15,0)
        layout.addWidget(self.ampPowerValue, 15,1)
        layout.addWidget(self.loadPowerLabel, 15,2)
        layout.addWidget(self.loadPowerValue, 15,3)

        #Temperature measurements
        self.tempLabel = QLabel('Temperature:')
        self.tempValue = QLabel('')
        #Add widgets to grid
        layout.addWidget(self.tempLabel, 16,0)
        layout.addWidget(self.tempValue, 16,1,1,3)
       
        #Impdance measurements
        self.impLabel = QLabel('Impedance:')
        self.impValue = QLabel('')
        #Add widgets to grid
        layout.addWidget(self.impLabel, 17,0)
        layout.addWidget(self.impValue, 17,1,1,3)

        #Error
        self.errorLabel = QLabel('Error:')
        self.errorValue = QLabel('None')
        #Add widgets to grid
        layout.addWidget(self.errorLabel, 18,0)
        layout.addWidget(self.errorValue, 18,1,1,3)

        #Save button
        self.saveButton = QPushButton('Save')
        layout.addWidget(self.saveButton, 19,0,1,4)
        self.saveButton.clicked.connect(lambda:self.addCommand('SAVE', ''))
        self.horizontalGroupBox.setLayout(layout)

    def updateViews(self):
        ## view has resized; update auxiliary views to match
        self.p2.setGeometry(self.p1.vb.sceneBoundingRect())
        self.p2.linkedViewChanged(self.p1.vb, self.p2.XAxis)
        self.p2g.setGeometry(self.p1g.vb.sceneBoundingRect())
        self.p2g.linkedViewChanged(self.p1g.vb, self.p2g.XAxis) 

    
    
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(sys.argv)
    sys.exit(app.exec_())

