import serial
import time

import numpy as np
import matplotlib.pyplot as plt

#--------Initialize Serial---------

serialDevice = '/dev/ttyUSB0'

ser = serial.Serial(serialDevice, 9600, timeout = 1, parity = serial.PARITY_NONE)
ser.flush()

print("Waiting for data from frequency counter....")
ser.read_all()
ser.read_until()

def serDataToFloat(serData):
    vals = serData.decode().split('.')
    out = float(vals[0])
    count = -1
    unitLabel = None
    for v in vals[1].split(','):
        #Check for unit
        spaceSplit = v.split(' ')
        
        strWithoutUnit = spaceSplit[0]
        if(len(spaceSplit) > 1):
            unitLabel = spaceSplit[1].replace('\r\n','')
        count -= len(strWithoutUnit)
        out += 10**(count)*float(strWithoutUnit)
    return out, unitLabel
        

#------------Plot----------------

data = []
times = []
timeStart = time.time()
ser.read_until()

for i in range(0,3):
    data.append(serDataToFloat(ser.read_until())[0])
    times.append(time.time()-timeStart)

fig, ax = plt.subplots(1)
line, = ax.plot(times,data)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (MHz)")
fig.show()

#Check when figure window is closed
while plt.fignum_exists(1):
    recv = serDataToFloat(ser.read_until())
    print(recv)
    data.append(recv[0])
    times.append(time.time()-timeStart)
    ax.set_xlim(0,times[-1])
    ax.set_ylim(min(data),max(data))
    line.set_ydata(data)
    line.set_xdata(times)
    fig.canvas.draw()
    fig.canvas.flush_events()