#!/usr/bin/env python

#
# python sample application that reads from the raspicomm's RS-232 Port
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

# read in a loop
print('start reading from the rs-232 port a maximum of ' + str(maxReadCount) + ' bytes')
readCount=0
while readCount < maxReadCount:
    readBuffer.append(ser.read(1))
    readCount=readCount+1

# print the received bytes
print('we received the following bytes:')
i=0
while i < maxReadCount:
    raw=readBuffer[i]
    val=ord(raw)
    hx=''
    if val >= 32 and val <= 126:
        hx=' - \'{0}\''.format(readBuffer[i])
    print('[{0:d}]: 0x{1:x}{2} --{3}--{4:d}'.format(i, val, hx, raw,val))    
    i=i+1
print readBuffer

