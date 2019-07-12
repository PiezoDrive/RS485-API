# RS485 API for PiezoDrive PDUS210

All commands and returns will use `\r` as a termination key. 

## Operational Commands 
### **Enable**
Enables the amplifier output.

|||
|-|-|
|Command|`ENABLE\r`|
|Notes|No return is given if amplifier will not enable, use the **Is Enabled** command to check. Clears overload errors.|

**Example** 

send: `ENABLE\r`

wait: 100 ms

send: `isENABLE\r`

Check response.
____
### **Disable**

Disable the amplifier output.

|||
|-|-|
|Command|`DISABLE\r`|
|Notes|No return is given if amplifier will not disable, use the **Is Enabled** command to check.|

**Example** 

send: `DISABLE\r`

wait: 100 ms

send: `isENABLE\r`

Check response.
____
### **Enable Phase Tracking**
Enables phase tracking.

|||
|-|-|
|Command|`enPHASE\r`| 
|Notes|No return is given if phase tracking is not enabled, use the **Is Phase Tracking** command to check.|

**Example** 

send: `enPHASE\r`

wait: 100 ms

send: `isPHASE\r`

Check response.
____
### **Disable Phase Tracking**
Disables phase tracking.

|||
|-|-|
|Command|`disPHASE\r`| 
|Notes|No return is given if phase tracking is not disabled, use the **Is Phase Tracking** command to check.|

**Example** 

send: `disPHASE\r`

wait: 100 ms

send: `isPHASE\r`

Check response.
____
### **Enable Power Tracking**
Enable power tracking.

|||
|-|-|
|Command|`enPOWER\r`| 
|Notes|No return is given if power tracking is not enabled, use the **Is Power Tracking** command to check.|

**Example** 

send: `enPOWER\r`

wait: 100 ms

send: `isPOWER\r`

Check response.
____
### **Disable Power Tracking**
Disable power tracking.

|||
|-|-|
|Command|`disPOWER\r`| 
|Notes|No return is given if power tracking is not disabled, use the **Is Power Tracking** command to check.|

**Example** 

send: `disPOWER\r`

wait: 100 ms

send: `isPOWER\r`

Check response.
____
### **Enable Current Tracking**
Enable current tracking.

|||
|-|-|
|Command|`enCURRENT\r`| 
|Notes|No return is given if current tracking is not enabled, use the **Is Current Tracking** command to check.|

**Example** 

send: `enCURRENT\r`

wait: 100 ms

send: `isCURRENT\r`

Check response.
____
### **Disable Power Tracking**
Disable current tracking.

|||
|-|-|
|Command|`disCURRENT\r`| 
|Notes|No return is given if current tracking is not disabled, use the **Is Current Tracking** command to check.|

**Example** 

send: `disCURRENT\r`

wait: 100 ms

send: `isCURRENT\r`

Check response.
____
### **Save Parameters**
Save current parameters to permanent storage.

|||
|-|-|
|Command|`SAVE\r`|
|Notes|The red led will flash slower when saving.|

**Example** 

send: `SAVE\r`

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
|Notes|No return is given if amplifier voltage is not set, use the **Get Output Voltage** command to check. **Note** Output voltage can't be changed while power tracking is enabled.|

**Example** 

send: `setVOLT100\r`

wait: 100 ms

send: `getVOLT\r`

Check response.
____
### **Set Output Frequency**
Sets the amplifier output frequency. 

|||
|-|-|
|Command|`setFREQ[frequency]\r`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|No return is given if amplifier frequency is not set, use the **Get Output Frequency** command to check. Will not update if phase tracking is enabled.|

**Example** 

send: `setFREQ50000\r`

wait: 100 ms

send: `getFREQ\r`

Check response.
____
### **Set Maximum Output Frequency**
Sets the amplifier maximum output frequency.

|||
|-|-|
|Command|`setMAXFREQ[frequency]\r`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|No return is given if amplifier maximum frequency is not set, use the **Get Maximum Frequency** command to check. Will limit the range of the frequency used for phase tracking.|

**Example** 

send: `setMAXFREQ55000\r`

wait: 100 ms

send: `getMAXFREQ\r`

Check response.
____
### **Set Minimum Output Frequency**
Sets the amplifier minimum output frequency.

|||
|-|-|
|Command|`setMINFREQ[frequency]\r`|
|Required| Frequency=[integer], frequency in Hz|
|Notes|No return is given if amplifier minimum frequency is not set, use the **Get Minimum Frequency** command to check. Will limit the range of the frequency used for phase tracking.|

**Example** 

send: `setMINFREQ45000\r`

wait: 100 ms

send: `getMINFREQ\r`

Check response.
____
### **Set Target Phase**
Sets the amplifier target phase.

|||
|-|-|
|Command|`setPHASE[phase]\r`|
|Required| Phase=[integer], phase in degrees|
|Notes|No return is given if amplifier target phase is not set, use the **Get Target Phase** command to check. Values larger than 180 or less than -180 will be ignored|

**Example** 

send: `setPHASE-10\r`

wait: 100 ms

send: `getPHASE\r`

Check response.
___

### **Set Maximum Load Power**
Sets the maximum power applied to the load.

|||
|-|-|
|Command|`setMAXLPOW[power]\r`|
|Required| Power=[integer], power in mW|
|Notes|No return is given if max load power is not set, use the **Get Maximum Load Power** command to check. Values larger than 210000 or less than 0 will be ignored| 

**Example** 

send: `setMAXLPOW100000\r`

wait: 100 ms

send: `getMAXLPOW\r`

Check response.
___

### **Set Target Power**
Sets the target power applied to the load.

|||
|-|-|
|Command|`setTARPOW[power]\r`|
|Required| Power=[integer], power in mW|
|Notes|No return is given if target power is not set, use the **Get Target Load Power** command to check. Values larger than max load power or less than 0 will be ignored| 

**Example** 

send: `setTARPOW90000\r`

wait: 100 ms

send: `getTARPOW\r`

Check response.
___

### **Set Current Power**
Sets the target current magnitude.

|||
|-|-|
|Command|`setCURRENT[current]\r`|
|Required| Power=[integer], current in mA|
|Notes|No return is given if target power is not set, use the **Get Current** command to check. Values larger than 20000 mA or less than 0 will be ignored| 

**Example** 

send: `setCURRENT1000\r`

wait: 100 ms

send: `getCURRENT\r`

Check response.
___

### **Set Phase Gain**
Sets the control gain used for phase tracking.

|||
|-|-|
|Command|`setPHASEGAIN[phase gain]\r`|
|Required| Phase gain=[integer] |
|Notes|No return is given if phase gain is not set, use the **Get Phase Gain** command to check. High values may result instability| 

**Example** 

send: `setPHASEGAIN1000\r`

wait: 100 ms

send: `getPHASEGAIN\r`

Check response.
___
### **Set Power Gain**
Sets the control gain used for power tracking.

|||
|-|-|
|Command|`setPOWERGAIN[power gain]\r`|
|Required| Power gain=[integer] |
|Notes|No return is given if power gain is not set, use the **Get Power Gain** command to check. High values may result instability| 

**Example** 

send: `setPOWERGAIN100\r`

wait: 100 ms

send: `getPOWERGAIN\r`

Check response.
___
### **Set Current Gain**
Sets the control gain used for current tracking.

|||
|-|-|
|Command|`setCURRENTGAIN[power gain]\r`|
|Required| Power gain=[integer] |
|Notes|No return is given if current gain is not set, use the **Get Power Gain** command to check. High values may result instability| 

**Example** 

send: `setCURRENTGAIN1000\r`

wait: 100 ms

send: `getCURRENTGAIN\r`

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

