import serial
import time
import sys

import numpy as np
import matplotlib.pyplot as plt

#--------Options------------------
accept_window = [124.5e6,125.5e6] #Set to none for no window
scale_unit = 1e6 #MHz

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

def readFreq():
    out = None
    while True:
            try:
                ser_in = ser.read_until()
            except KeyboardInterrupt:
                print("Tootles!")
                sys.exit()
            if(len(ser_in)>0):
                try:
                    out = serDataToFloat(ser_in)
                except ValueError:
                    print("Bad value from frequency counter : "+ser_in.decode())
                    continue
            else:
                print("Timeout or empty value received!");
                continue
            if(accept_window is not None):
                if(accept_window[0] <= out[0]*scale_unit <= accept_window[1]):
                    return out
                else:
                    print("Value %.3f out of expected range of " % out[0] + str(accept_window))
    

#------------Plot----------------

data = []
times = []
timeStart = time.time()
ser.read_until()

for i in range(0,3):
    data.append(readFreq()[0]*scale_unit)
    times.append(time.time()-timeStart)

fig, ax = plt.subplots(1)
line, = ax.plot(times,data)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")
fig.show()

#Check when figure window is closed
while plt.fignum_exists(1):
    recv = readFreq()
    print(recv)
    data.append(recv[0]*scale_unit)
    times.append(time.time()-timeStart)
    ax.set_xlim(0,times[-1])
    ax.set_ylim(min(data),max(data))
    line.set_ydata(data)
    line.set_xdata(times)
    fig.canvas.draw()
    fig.canvas.flush_events()

