# RS485 API for PiezoDrive PDUS210

## Version 300000 firmware or higher

* All commands except for getSTATE and getSTATEWAVE and returns will use `\r` as a termination key. 

* getSTATE will return a buffer that is 80 bytes.
* getSTATEWAVE will return a buffer that is 2080 bytes.
* Baud rates of 9600, 115200, 460800, 921600 are selectable through the desktop software, with the default being 9600. It is recommended that 921600 is used if using the getSTATEWAVE command.
* Allow 2.5 ms between commands

## Operational Commands 
### **Enable**
Enables the amplifier output.

|||
|-|-|
|Command|`ENABLE\r`|
|Notes|Will return the new value. Clears overload errors.|

**Example** 

send: `ENABLE\r`

read: `TRUE\r`
____
### **Disable**

Disable the amplifier output.

|||
|-|-|
|Command|`DISABLE\r`|
|Notes|Will return the new value.|

**Example** 

send: `DISABLE\r`

read: `FALSE\r`
### **Enable Phase Tracking**
Enables phase tracking.

|||
|-|-|
|Command|`enPHASE\r`| 
|Notes|New value is returned.|

**Example** 

send: `enPHASE\r`

read: `TRUE\r`
____
### **Disable Phase Tracking**
Disables phase tracking.

|||
|-|-|
|Command|`disPHASE\r`| 
|Notes|New value is returned.|

**Example** 

send: `disPHASE\r`

read: `FALSE\r`
____
### **Enable Power Tracking**
Enable power tracking.

|||
|-|-|
|Command|`enPOWER\r`| 
|Notes|New value is returned. Disables current tracking.|

**Example** 

send: `enPOWER\r`

read: `TRUE\r`
____
### **Disable Power Tracking**
Disable power tracking.

|||
|-|-|
|Command|`disPOWER\r`| 
|Notes|New value is returned.|

**Example** 

send: `disPOWER\r`

read: `FALSE\r`
____
### **Enable Current Tracking**
Enable current tracking.

|||
|-|-|
|Command|`enCURRENT\r`| 
|Notes|New value is returned. Disables power tracking.|

**Example** 

send: `enCURRENT\r`

read: `TRUE\r`
____
### **Disable Power Tracking**
Disable current tracking.

|||
|-|-|
|Command|`disCURRENT\r`| 
|Notes|New value is returned.|

**Example** 

send: `disCURRENT\r`

read: `FALSE\r`
____
### **Save Parameters**
Save current parameters to permanent storage.

|||
|-|-|
|Command|`SAVE\r`|
|Notes|Returns `TRUE\r` when complete|

**Example** 

send: `SAVE\r`

read: `TRUE\r`

## Operational Queries
### **Is Enabled**
Queries if the amplifier is enabled.

|||
|-|-|
|Command|`isENABLE\r`|
|Returns|`TRUE\r` or `FALSE\r`|

**Example** 

send: `isENABLE\r`

receive: `TRUE\r`
____
### **Is Phase Tracking**
Queries if phase tracking is enabled.

|||
|-|-|
|Command|`isPHASE\r`|
|Returns|`TRUE\r` or `FALSE\r`|

**Example** 

send: `isPHASE\r`

receive: `TRUE\r`
____
### **Is Power Tracking**
Queries if power tracking is enabled.

|||
|-|-|
|Command|`isPOWER\r`|
|Returns|`TRUE\r` or `FALSE\r`|

**Example** 

send: `isPOWER\r`

receive: `TRUE\r`
____

### **Is Current Tracking**
Queries if current tracking is enabled.

|||
|-|-|
|Command|`isCURRENT\r`|
|Returns|`TRUE\r` or `FALSE\r`|

**Example** 

send: `isCURRENT\r`

receive: `TRUE\r`
____


## Set Control Parameters
### **Set Output Voltage**
Sets the amplifier output voltage. 

|||
|-|-|
|Command|`setVOLT[voltage]\r`|
|Required| Voltage=[integer], peak to peak voltage in volts|
|Notes|New value is returned. Clipped between 0 and the maximum voltage output. **Note** Output voltage can't be changed while power tracking or current tracking is enabled.|

**Example** 

send: `setVOLT100\r`

read: `100\r`
____
### **Set Output Frequency**
Sets the amplifier output frequency. 

|||
|-|-|
|Command|`setFREQ[frequency]\r`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|New value is returned. Clipped between the minimum and maximum frequency. Will not update if phase tracking is enabled.|

**Example** 

send: `setFREQ50000\r`

read: `50000\r`
____
### **Set Maximum Output Frequency**
Sets the amplifier maximum output frequency.

|||
|-|-|
|Command|`setMAXFREQ[frequency]\r`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|New value is returned. Clipped between the minimum frequency and 520000 Hz. Will limit the range of the frequency used for phase tracking.|

**Example** 

send: `setMAXFREQ55000\r`

read: `55000\r`
____
### **Set Minimum Output Frequency**
Sets the amplifier minimum output frequency.

|||
|-|-|
|Command|`setMINFREQ[frequency]\r`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|New value is returned. Clipped between 5400 Hz and the maximum frequency. Will limit the range of the frequency used for phase tracking.|

**Example** 

send: `setMINFREQ45000\r`

read: `45000\r`

____
### **Set Target Phase**
Sets the amplifier target phase.

|||
|-|-|
|Command|`setPHASE[phase]\r`|
|Required| Phase=[integer], phase in degrees|
|Notes|New value is returned. Clipped between -180 and 180|

**Example** 

send: `setPHASE-10\r`

read: `-10\r`
___

### **Set Maximum Load Power**
Sets the maximum power applied to the load.

|||
|-|-|
|Command|`setMAXLPOW[power]\r`|
|Required| Power=[integer], power in mW|
|Notes|New value is returned. Clipped between 0 and 210000 mW| 

**Example** 

send: `setMAXLPOW100000\r`

read: `100000\r`

___

### **Set Target Power**
Sets the target power applied to the load.

|||
|-|-|
|Command|`setTARPOW[power]\r`|
|Required| Power=[integer], power in mW|
|Notes|New value is returned. Clipped between 0 and maximum load power| 

**Example** 

send: `setTARPOW90000\r`

read: `90000\r`

___

### **Set Target Current**
Sets the target current magnitude.

|||
|-|-|
|Command|`setCURRENT[current]\r`|
|Required| Power=[integer], current in mA|
|Notes|New value is returned. Clipped between 0 and 20000 mA| 

**Example** 

send: `setCURRENT1000\r`

read: `1000\r`

___

### **Set Phase Gain**
Sets the control gain used for phase tracking.

|||
|-|-|
|Command|`setPHASEGAIN[phase gain]\r`|
|Required| Phase gain=[integer] |
|Notes|New value is returned. Clipped between -100000 and 100000| 

**Example** 

send: `setPHASEGAIN1000\r`

read: `1000\r`
___
### **Set Power Gain**
Sets the control gain used for power tracking.

|||
|-|-|
|Command|`setPOWERGAIN[power gain]\r`|
|Required| Power gain=[integer] |
|Notes|New value is returned. Clipped between 0 and 100000| 

**Example** 

send: `setPOWERGAIN100\r`

read: `100\r`

___
### **Set Current Gain**
Sets the control gain used for current tracking.

|||
|-|-|
|Command|`setCURRENTGAIN[power gain]\r`|
|Required| Power gain=[integer] |
|Notes|New value is returned. Clipped between 0and 100000| 

**Example** 

send: `setCURRENTGAIN1000\r`

read: `1000\r`

Check response.
___
## Get Control Parameters
### **Get Output Voltage**
Returns the amplifier output voltage. 

|||
|-|-|
|Command|`getVOLT\r`|
|Returns|peak to peak voltage in V|

**Example**
send: `getVOLT\r`

receive: `100\r`
____
### **Get Output Frequency**
Returns the amplifier output frequency. 

|||
|-|-|
|Command|`getFREQ\r`|
|Returns|Frequency in Hz|

**Example**

send: `getFREQ\r`

receive: `80000\r`
____
### **Get Maximum Frequency**
Returns the amplifier maximum output frequency. 

|||
|-|-|
|Command|`getMAXFREQ\r`|
|Returns|Maximum frequency in Hz|

**Example**

send: `getMAXFREQ\r`

receive: `90000\r`
____
### **Get Minimum Frequency**
Returns the amplifier minimum output frequency.

|||
|-|-|
|Command|`getMINFREQ\r`|
|Returns|Minimum frequency in Hz|

**Example**

send: `getMINFREQ\r`

receive: `70000\r`
____
### **Get Target Phase**
Returns the target phase.

|||
|-|-|
|Command|`getPHASE\r`|
|Returns|Phase in degrees|

**Example**

send: `getPHASE\r`

receive: `-10\r`
____
### **Get Maximum Load Power**
Returns the maximum load power. 

|||
|-|-|
|Command|`getMAXLPOW\r`|
|Returns|Power in mW|

**Example**

send: `getMAXLPOW\r`

receive: `100000\r`
____
### **Get Target Load Power**
Returns the target load power. 

|||
|-|-|
|Command|`getTARPOW\r`|
|Returns|Power in mW|

**Example**

send: `getTARPOW\r`

receive: `90000\r`
____
### **Get Phase Gain**
Returns the phase tracking control gain. 

|||
|-|-|
|Command|`getPHASEGAIN\r`|
|Returns|Gain|

**Example**

send:` getPHASEGAIN\r`

receive: `1000\r`
____
### **Get Power Gain**
Returns the set power tracking control gain. 

|||
|-|-|
|Command|`getPOWERGAIN\r`|
|Returns|Gain|

**Example**

send: `getPOWERGAIN\r`

receive: `200\r`
____
### **Get Current**
Returns the set current. 

|||
|-|-|
|Command|`getCURRENT\r`|
|Returns|Current in mA|

**Example**

send: `getCURRENT\r`

receive: `1000\r`
____

## Read Measured Values
### Read Measured Phase
Returns the measured phase.

|||
|-|-|
|Command|`readPHASE\r`|
|Returns|Phase in degrees|

**Example**

send: `readPHASE\r`

receive: `11\r`
___
### Read Measured Impedance
Returns the measured impedance.

|||
|-|-|
|Command|`readIMP\r`|
|Returns|Load impedance in ohms|

**Example**

send: `readIMP\r`

receive: `220\r`
____
### Read Load Power
Returns the measured load power.

|||
|-|-|
|Command|`readLPOW\r`|
|Returns|Power in mW|

**Example**

send: `readLPOW\r`

receive: `91230\r`
____
### Read Amplifier Power
Returns power dissipated via the amplifier.

|||
|-|-|
|Command|`readAPOW\r`|
|Returns|Power in mW|

**Example**

send: `readAPOW\r`

receive: `111230\r`
___
### Read Current
Returns measured current magnitude.

|||
|-|-|
|Command|`readCURRENT\r`|
|Returns|Current in mA|

**Example**

send: `readCURRENT\r`

receive: `1033\r`
___
### Read Amplifier Temperature
Returns the measured amplifier temperature.

|||
|-|-|
|Command|`readTEMP\r`|
|Returns|temperature in celsius|

**Example**

send: `readTEMP\r`

receive: `42\r`

## Errors


### Communication Error

Error will occur when corrupted commands are sent to the amplifier via RS485. It is suggested to resend the command.

|||
|-|-|
|Message|`TXERR\r`|
____

### Load Overload Error

Error will occur when load power exceeds the set load power value. Is sent 10 times at 100 ms intervals to insure it is received. Is reset via the **Enable** command. 

|||
|-|-|
|Message|`LPERR\r`|
|Reset|`ENABLE\r`|

**Example**

receive: `LPERR\r`

wait: 2 s 

send: `ENABLE\r`
____
### Amplifier Overload Error

Error will occur when amplifier dissipation power exceeds set value. Is sent 10 times at 100 ms intervals to insure it is received. Is reset via the **Enable** command. 

|||
|-|-|
|Message|`APERR\r`|
|Reset|`ENABLE\r`|

**Example**

receive: `APERR\r`

wait: 2 s 

send: `ENABLE\r`
___
### Amplifier Temperature Error

Error will occur when amplifier temperature exceeds set value. Is sent 10 times at 100 ms intervals to insure it is received. Is reset via the **Enable** command. 

|||
|-|-|
|Message|`ATERR\r`|
|Reset|`ENABLE\r`|

**Example**

receive: `ATERR\r`

wait: 2 s 

send: `ENABLE\r`
___

### Disable Error Reporting

Disables the reporting of the load overload, amplifier overload and temperature overload errors. To used when using the **getSTATE** command to monitor for errors. Returns TRUE when updated. See examples: 
* sweep_example.py
* state_example.py
* gui_example.py 

|||
|-|-|
|Command|`disERROR\r`|

**Example**

send: `disERROR\r`

receive: `TRUE\r`
____
## Get Amplifier state

### Get state 
Returns the current state of the amplifier as a buffer. See examples:
* sweep_example.py
* state_example.py

|||
|-|-|
|Command|`getSTATE\r`|
|Returns|Buffer 80 bytes long|

#### structure

In order as shown in table
|Type|Name|Units|
|-|-|-|
|char|enabled||
|char|power tracking||
|char|current tracking||
|char|powerTracking||
|char|error amp||
|char|error load||
|char|error temperature|| 
|char|padding|| 
|float|voltage|V peak-peak |
|float|frequency|Hz| 
|float|min frequency|Hz| 
|float|max frequency|Hz|
|float|target phase|Deg|
|float|phase control gain||
|float|target current|mA|
|float|current control gain| 
|float|target power|W|
|float|power control gain||
|float|max load power|W|
|float|amplifier power|W|
|float|load power|W|
|float|temperature|C|
|float|measured phase|Deg|
|float|measured current|mA peak|
|float|impedance|Ohms|
|float|transformer turns||

___

### Get state with waveform
Returns the current state of the amplifier and voltage and current waveforms as a buffer. See examples:
* gui_example.py

|||
|-|-|
|Command|`getSTATEWAVE\r`|
|Returns|Buffer 2080 bytes long|

#### structure

In order as shown in table
|Type|Name|Units|
|-|-|-|
|char|enabled||
|char|power tracking||
|char|current tracking||
|char|powerTracking||
|char|error amp||
|char|error load||
|char|error temperature|| 
|char|padding|| 
|float|voltage|V peak-peak |
|float|frequency|Hz| 
|float|min frequency|Hz| 
|float|max frequency|Hz|
|float|target phase|Deg|
|float|phase control gain||
|float|target current|mA|
|float|current control gain| 
|float|target power|W|
|float|power control gain||
|float|max load power|W|
|float|amplifier power|W|
|float|load power|W|
|float|temperature|C|
|float|measured phase|Deg|
|float|measured current|mA peak|
|float|impedance|Ohms|
|float|transformer turns||
|float[250]|voltage waveform|V|
|float[250]|current waveform|A|
___