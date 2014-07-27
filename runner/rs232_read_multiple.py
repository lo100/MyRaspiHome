#!/usr/bin/env python

#
# python sample application that reads serial data from RX/TX - GPIO ports
#

import array
import serial

maxReadCount=105
readBuffer = array.array('c')

print('this sample application reads from the rs-232 port')

# open the port
print('opening device /dev/ttyAMA0')
try:
    ser = serial.Serial(port='/dev/ttyAMA0', baudrate=4800)
    ser.parity = 'N'
    ser.stoppbits = 1
    ser.bytesize = 8
    ser.flowcontrol = 'off'
except:
    print('failed.')
    print('possible causes:')
    print('1) the raspicomm device driver is not loaded. type \'lsmod\' and verify that you \'raspicommrs232\' is loaded.')
    print('2) the raspicomm device driver is in use. Is another application using the device driver?')
    print('3) something went wrong when loading the device driver. type \'dmesg\' and check the kernel messages')
    exit()

print('successful.')

# print the received bytes
print('we received the following bytes:')
logfile = file('logfile.txt','w')
while True:
    data = ser.readline()
    print(data)
    logfile.write(data)
    logfile.flush()
logfile.close()

    

