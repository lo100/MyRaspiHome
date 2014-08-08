#!/usr/bin/env python

#
# python application that reads tarom solar charger logfiles and saves data to hdf5 files
#
import sys
import os
from data_mapper.data_mapper_interface import DataMapperInterface
from data_mapper.data_mapper_tarom import DataMapperTarom
from data_accessor.data_accessor_hdf5 import DataAccessorHDF5
from common.time import get_offset 

# open logfile
log_filename = sys.argv[1]

# add line by line to list - remove duplicates
previous_time = None
recordings = []
print('Open logfile: ' + log_filename)
with open(log_filename, 'r') as logfile:
    for line in logfile:
        # check for duplicates
        values = line.split(';')
        if values[2] == previous_time:
            print('Duplicate Time found ' + values[1] + ' ' + values[2])
        else:
            recordings.append(line)
        previous_time = values[2]
    
# map data
print('Map data')
dm = DataMapperInterface('tarom')
data = dm.map(recordings)

# write mapped data to HDF5 file
da = DataAccessorHDF5()

# initialize variables
current_year = 1970
current_month = 01
current_day = 01
offset = 0
index = 0
lastindex = len(data) - 1
timeoffset = 0
hdfDate = None


for sample in data:
    date = sample['Date'].split('/')
    
    if index == 0:
        # initialize variables - first sample
        current_year = int(date[0])
        current_month = int(date[1])
        current_day = int(date[2])
        timeoffset = get_offset(sample['Time'] + ':00', DataMapperTarom.FREQUENCY)
        hdfDate = ''.join(date)
        folderDate = '\\'.join(date[0:2])
        
    if int(date[0]) != current_year or int(date[1]) != current_month or int(date[2]) != current_day or index == lastindex:
        # write data to HDF5 file
        folderName = 'E:\\home\\' + folderDate
        if not os.path.exists(folderName):
            os.makedirs(folderName)
        hdf5_filename = folderName + '\\logfile_' + hdfDate + '.hdf5'
        print('Open HDF5: ' + hdf5_filename)
        da.open(hdf5_filename, 'a')
        da.write('tarom', data[offset:index], DataMapperTarom.DATA_CONFIGURATION, timeoffset, 1440)
        print('Total added ' + str(index - offset) + ' samples for ' + str(current_year) + '-' + str(current_month) + '-' + str(current_day))
        da.close()
        
        # calculations for next HDF5 file
        current_year = int(date[0])
        current_month = int(date[1])
        current_day = int(date[2])
        offset = index
        timeoffset = get_offset(sample['Time'] + ':00', DataMapperTarom.FREQUENCY)
        hdfDate = ''.join(date)
        folderDate = '\\'.join(date[0:2])

    index += 1
