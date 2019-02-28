# RS485 API for PiezoDrive PDus210

All commands and returns will use `\n` as a termination key. 

## Operational Commands 
### **Enable**
Enables the amplifier output.

|||
|-|-|
|Command|`ENABLE\n`|
|Notes|No return is given if amplifier will not enable, use the **Is Enabled** command to check. Clears overload errors.|

**Example** 

send: `ENABLE\n`

wait: 100 ms

send: `isENABLE\n`

Check response.
____
### **Disable**

Disable the amplifier output.

|||
|-|-|
|Command|`DISABLE\n`|
|Notes|No return is given if amplifier will not disable, use the **Is Enabled** command to check.|

**Example** 

send: `DISABLE\n`

wait: 100 ms

send: `isENABLE\n`

Check response.
____
### **Enable Phase Tracking**
Enables phase tacking.

|||
|-|-|
|Command|`enPHASE\n`| 
|Notes|No return is given if phase tacking is not enabled, use the **Is Phase Tracking** command to check.|

**Example** 

send: `enPHASE\n`

wait: 100 ms

send: `isPHASE\n`

Check response.
____
### **Disable Phase Tracking**
Disables phase tacking.

|||
|-|-|
|Command|`disPHASE\n`| 
|Notes|No return is given if phase tacking is not disabled, use the **Is Phase Tracking** command to check.|

**Example** 

send: `disPHASE\n`

wait: 100 ms

send: `isPHASE\n`

Check response.
____
### **Enable Power Tracking**
Enable power tacking.

|||
|-|-|
|Command|`enPOWER\n`| 
|Notes|No return is given if power tacking is not enabled, use the **Is Power Tracking** command to check.|

**Example** 

send: `enPOWER\n`

wait: 100 ms

send: `isPOWER\n`

Check response.
____
### **Disable Power Tracking**
Disable power tacking.

|||
|-|-|
|Command|`disPOWER\n`| 
|Notes|No return is given if power tacking is not disabled, use the **Is Power Tracking** command to check.|

**Example** 

send: `disPOWER\n`

wait: 100 ms

send: `isPOWER\n`

Check response.
____
### **Save Parameters**
Save current parameters to permanent storage.

|||
|-|-|
|Command|`SAVE\n`|
|Notes|The red led will flash slower when saving.|

**Example** 

send: `SAVE\n`

## Operational Queries
### **Is Enabled**
Queries if the amplifier is enabled.

|||
|-|-|
|Command|`isENABLE\n`|
|Returns|`TRUE\n` or `FALSE\n`|

**Example** 

send: `isENABLE\n`

receive: `TRUE\n`
____
### **Is Phase Tracking**
Queries if phase tracking is enabled.

|||
|-|-|
|Command|`isPHASE\n`|
|Returns|`TRUE\n` or `FALSE\n`|

**Example** 

send: `isPHASE\n`

receive: `TRUE\n`
____
### **Is Power Tacking**
Queries if power tacking is enabled.

|||
|-|-|
|Command|`isPOWER\n`|
|Returns|`TRUE\n` or `FALSE\n`|

**Example** 

send: `isPOWER\n`

receive: `TRUE\n`
____

## Set Control Parameters
### **Set Output Voltage**
Sets the amplifier output voltage. 

|||
|-|-|
|Command|`setVOLT[voltage]\n`|
|Required| Voltage=[integer], peak to peak voltage in volts|
|Notes|No return is given if amplifier voltage is not set, use the **Get Output Voltage** command to check. **Note** Output voltage can't be changed while power tracking is enabled.|

**Example** 

send: `setVOLT100\n`

wait: 100 ms

send: `getVOLT\n`

Check response.
____
### **Set Output Frequency**
Sets the amplifier output frequency. 

|||
|-|-|
|Command|`setFREQ[frequency]\n`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|No return is given if amplifier frequency is not set, use the **Get Output Frequency** command to check. Will not update if phase tracking is enabled.|

**Example** 

send: `setFREQ50000\n`

wait: 100 ms

send: `getFREQ\n`

Check response.
____
### **Set Maximum Output Frequency**
Sets the amplifier maximum output frequency.

|||
|-|-|
|Command|`setMAXFREQ[frequency]\n`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|No return is given if amplifier maximum frequency is not set, use the **Get Maximum Frequency** command to check. Will limit the range of the frequency used for phase tracking.|

**Example** 

send: `setMAXFREQ55000\n`

wait: 100 ms

send: `getMAXFREQ\n`

Check response.
____
### **Set Minimum Output Frequency**
Sets the amplifier minimum output frequency.

|||
|-|-|
|Command|`setMINFREQ[frequency]\n`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|No return is given if amplifier minimum frequency is not set, use the **Get Minimum Frequency** command to check. Will limit the range of the frequency used for phase tracking.|

**Example** 

send: `setMINFREQ45000\n`

wait: 100 ms

send: `getMINFREQ\n`

Check response.
____
### **Set Target Phase**
Sets the amplifier target phase.

|||
|-|-|
|Command|`setPHASE[phase]\n`|
|Required| Phase=[integer], phase in degrees|
|Notes|No return is given if amplifier target phase is not set, use the **Get Target Phase** command to check. Values larger than 180 or less than -180 will be ignored|

**Example** 

send: `setPHASE-10\n`

wait: 100 ms

send: `getPHASE\n`

Check response.
___

### **Set Maximum Load Power**
Sets the maximum power applied to the load.

|||
|-|-|
|Command|`setMAXLPOW[power]\n`|
|Required| Power=[integer], power in mW|
|Notes|No return is given if max load power is not set, use the **Get Maximum Load Power** command to check. Values larger than 210000 or less than 0 will be ignored| 

**Example** 

send: `setMAXLPOW100000\n`

wait: 100 ms

send: `getMAXLPOW\n`

Check response.
___

### **Set Target Power**
Sets the target power applied to the load.

|||
|-|-|
|Command|`setTARPOW[power]\n`|
|Required| Power=[integer], power in mW|
|Notes|No return is given if target power is not set, use the **Get Target Load Power** command to check. Values larger than max load power or less than 0 will be ignored| 

**Example** 

send: `setTARPOW90000\n`

wait: 100 ms

send: `getTARPOW\n`

Check response.
___

### **Set Phase Gain**
Sets the control gain used for phase tracking.

|||
|-|-|
|Command|`setPHASEGAIN[phase gain]\n`|
|Required| Phase gain=[integer] |
|Notes|No return is given if phase gain is not set, use the **Get Phase Gain** command to check. High values may result instability| 

**Example** 

send: `setPHASEGAIN1000\n`

wait: 100 ms

send: `getPHASEGAIN\n`

Check response.
___
### **Set Power Gain**
Sets the control gain used for power tracking.

|||
|-|-|
|Command|`setPOWERGAIN[power gain]\n`|
|Required| Power gain=[integer] |
|Notes|No return is given if power gain is not set, use the **Get Power Gain** command to check. High values may result instability| 

**Example** 

send: `setPOWERGAIN100\n`

wait: 100 ms

send: `getPOWERGAIN\n`

Check response.
___
## Get Control Parameters
### **Get Output Voltage**
Returns the amplifier output voltage. 

|||
|-|-|
|Command|`getVOLT\n`|
|Returns|peak to peak voltage in V|

**Example**
send: `getVOLT\n`

receive: `100\n`
____
### **Get Output Frequency**
Returns the amplifier output frequency. 

|||
|-|-|
|Command|`getFREQ\n`|
|Returns|Frequency in Hz|

**Example**

send: `getFREQ\n`

receive: `80000\n`
____
### **Get Maximum Frequency**
Returns the amplifier maximum output frequency. 

|||
|-|-|
|Command|`getMAXFREQ\n`|
|Returns|Maximum frequency in Hz|

**Example**

send: `getMAXFREQ\n`

receive: `90000\n`
____
### **Get Minimum Frequency**
Returns the amplifier minimum output frequency.

|||
|-|-|
|Command|`getMINFREQ\n`|
|Returns|Minimum frequency in Hz|

**Example**

send: `getMINFREQ\n`

receive: `70000\n`
____
### **Get Target Phase**
Returns the target phase.

|||
|-|-|
|Command|`getPHASE\n`|
|Returns|Phase in degrees|

**Example**

send: `getPHASE\n`

receive: `-10\n`
____
### **Get Maximum Load Power**
Returns the maximum load power. 

|||
|-|-|
|Command|`getMAXLPOW\n`|
|Returns|Power in mW|

**Example**

send: `getMAXLPOW\n`

receive: `100000\n`
____
### **Get Target Load Power**
Returns the target load power. 

|||
|-|-|
|Command|`getTARPOW\n`|
|Returns|Power in mW|

**Example**

send: `getTARPOW\n`

receive: `90000\n`
____
### **Get Phase Gain**
Returns the phase tracking control gain. 

|||
|-|-|
|Command|`getPHASEGAIN\n`|
|Returns|Gain|

**Example**

send:` getPHASEGAIN\n`

receive: `1000\n`
____
### **Get Power Gain**
Returns the set power tracking control gain. 

|||
|-|-|
|Command|`getPOWERGAIN\n`|
|Returns|Gain|

**Example**

send: `getPOWERGAIN\n`

receive: `200\n`
____

## Read Measured Values
### Read Measured Phase
Returns the measured phase.

|||
|-|-|
|Command|`readPHASE\n`|
|Returns|Phase in degrees|

**Example**

send: `readPHASE\n`

receive: `11\n`
___
### Read Measured Impedance
Returns the measured impedance.

|||
|-|-|
|Command|`readIMP\n`|
|Returns|Load impedance in ohms|

**Example**

send: `readIMP\n`

receive: `220\n`
____
### Read Load Power
Returns the measured load power.

|||
|-|-|
|Command|`readLPOW\n`|
|Returns|Power in mW|

**Example**

send: `readLPOW\n`

receive: `91230\n`
____
### Read Amplifier Power
Returns power dissipated via the amplifier.

|||
|-|-|
|Command|`readAPOW\n`|
|Returns|Power in mW|

**Example**

send: `readAPOW\n`

receive: `111230\n`
___
### Read Amplifier Temperature
Returns the measured amplifier temperature.

|||
|-|-|
|Command|`readTEMP\n`|
|Returns|temperature in celsius|

**Example**

send: `readTEMP\n`

receive: `42\n`

## Errors

### Communication Error

Error will occur when corrupted commands are sent to the amplifier via RS485. It is suggested to resend the command.

|||
|-|-|
|Message|`TXERR\n`|
____

### Load Overload Error

Error will occur when load power exceeds the set load power value. Is sent 10 times at 100 ms intervals to insure it is received. Is reset via the **Enable** command. 

|||
|-|-|
|Message|`LPERR\n`|
|Reset|`ENABLE\n`|

**Example**

receive: `LPERR\n`

wait: 2 s 

send: `ENABLE\n`
____
### Amplifier Overload Error

Error will occur when amplifier dissipation power exceeds set value. Is sent 10 times at 100 ms intervals to insure it is received. Is reset via the **Enable** command. 

|||
|-|-|
|Message|`APERR\n`|
|Reset|`ENABLE\n`|

**Example**

receive: `APERR\n`

wait: 2 s 

send: `ENABLE\n`
___
### Amplifier Temperature Error

Error will occur when amplifier temperature exceeds set value. Is sent 10 times at 100 ms intervals to insure it is received. Is reset via the **Enable** command. 

|||
|-|-|
|Message|`ATERR\n`|
|Reset|`ENABLE\n`|

**Example**

receive: `ATERR\n`

wait: 2 s 

send: `ENABLE\n`

