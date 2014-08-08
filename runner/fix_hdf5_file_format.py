#!/usr/bin/env python

#
# Fix HDF5 files and add mandatory attributes for support PyTables file format 
#

import h5py
import sys

# open HDF5 file
hdf5_filename = sys.argv[1]
hdf5_file = h5py.File(hdf5_filename, 'a')

# add mandatory attributes for a file
hdf5_file['/'].attrs['CLASS'] = 'GROUP'
hdf5_file['/'].attrs['PYTABLES_FORMAT_VERSION'] = '2.1'
hdf5_file['/'].attrs['TITLE'] = 'Root element'
hdf5_file['/'].attrs['VERSION'] = '1.0'

# add mandatory attributes for a group
groups = ('/series', '/series/tarom')

for group in groups:
    hdf5_file[group].attrs['CLASS'] = 'GROUP'
    hdf5_file[group].attrs['TITLE'] = 'groupnode'
    hdf5_file[group].attrs['VERSION'] = '1.0'  


# add mandatory attributes for leaves
for group in hdf5_file['/series/tarom'].keys():
    node = '/series/tarom/' + group
    hdf5_file[node].attrs['CLASS'] = 'GROUP'
    hdf5_file[node].attrs['TITLE'] = 'groupnode'
    hdf5_file[node].attrs['VERSION'] = '1.0'
    
    hdf5_file[node + '/data'].attrs['CLASS'] = 'ARRAY'
    hdf5_file[node + '/data'].attrs['TITLE'] = 'data array'
    hdf5_file[node + '/data'].attrs['VERSION'] = '2.4'
    
    hdf5_file[node + '/mask'].attrs['CLASS'] = 'ARRAY'
    hdf5_file[node + '/mask'].attrs['TITLE'] = 'mask array'
    hdf5_file[node + '/mask'].attrs['VERSION'] = '2.4'
    
    
# close HDF5 file
hdf5_file.close()
