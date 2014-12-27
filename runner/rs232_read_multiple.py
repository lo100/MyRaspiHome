#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

"""
module:: runner
:synopsis: Application that reads data from Steca Tarom solar charger using
the RS-232 interface.

moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>

License: MIT (http://opensource.org/licenses/MIT)

Start the script:
$ python rs232_read_multiple.py
"""

import array
import serial

from time import gmtime, strftime

maxReadCount = 105
readBuffer = array.array('c')

print 'Connect to Steca Tarom solar charger'

# open the port
print 'Opening device /dev/ttyAMA0'
try:
    ser = serial.Serial(port='/dev/ttyAMA0', baudrate=4800)
    ser.parity = 'N'
    ser.stoppbits = 1
    ser.bytesize = 8
    ser.flowcontrol = 'off'
except:
    print 'ERROR could not connect to Steca Tarom solar charger!'
    print 'Possible causes:'
    print '1) the serial device is in use. Is another application using the device ttyAMA0?'
    print '2) something went wrong when loading the device driver. type \'dmesg\' and check the kernel messages'
    exit()

print 'successful.'

filename = '/var/log/solar/log_' + strftime("%Y%m%d_%H%M%S", gmtime()) + '.txt'
logfile = file(filename, 'w')

# print the received bytes
print 'INFO start reading data from Steca Tarom solar charger'
while True:
    data = ser.readline()
    # print data
    logfile.write(data)
    logfile.flush()
logfile.close()


