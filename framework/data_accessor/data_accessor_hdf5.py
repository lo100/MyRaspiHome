"""
   module:: data_accessor
   :synopsis: Data accessor for HDF5 files.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""
import h5py
import numpy as np

from data_accessor.exceptions import DataAccessorError

class DataAccessorHDF5():

    """The HDF5 file.
    """
    _file = None

    """Data accessor type.
    """
    DATA_ACCESSOR_TYPE = 'hdf5'

    def __init__(self):
        pass

    def _create_root_node(self):
        # create root node if not exist
        root_node = 'series'
        if root_node not in self._file['/'].keys():
            self._file['/'].attrs['CLASS'] = 'GROUP'
            self._file['/'].attrs['PYTABLES_FORMAT_VERSION'] = '2.1'
            self._file['/'].attrs['TITLE'] = 'Root element'
            self._file['/'].attrs['VERSION'] = '1.0'
            self._file.create_group(root_node)
            group_node = '/' + root_node
            self._file[group_node].attrs['CLASS'] = 'GROUP'
            self._file[group_node].attrs['TITLE'] = 'groupnode'
            self._file[group_node].attrs['VERSION'] = '1.0' 
        return '/' + root_node
    
    def _create_source_node(self, source=None):
        # create source node if not exist
        root_node = self._create_root_node()
        source_node = root_node
        if source != None:
            source_node += '/' + source
            if source not in self._file[root_node].keys():
                self._file.create_group(source_node)
                self._file[source_node].attrs['CLASS'] = 'GROUP'
                self._file[source_node].attrs['TITLE'] = 'groupnode'
                self._file[source_node].attrs['VERSION'] = '1.0'  
        return source_node
            
    def open(self, filename, mode='a'):
        """ Opens the hdf5 file used by the data accessor.
        
        :param filename: Name of the file to be opened (including path).
        :type filename: string
        :param mode: File open mode.
        :type mode: string
        :rtype: boolean
        """
        try:
            self._file = h5py.File(filename, mode)
        except:
            raise DataAccessorError('HDF5 file could not be opened! ' + filename)

    def close(self):
        """ Closes the HDF5 file.
        
        :rtype: boolean
        """
        self._file.close()
        return True

    def read(self, source=None, parameter=(), offset=None, length=None):
        """Reads from the HDF5 file.
        
        :param source: The data source (device).
        :type source: string
        :param parameter: A list of parameter to be read.
        :type parameter: string list
        :param offset: offset to start reading data.
        :type offset: integer
        :param length: max number off values per parameter to be read.
        :type length: integer       
        :rtype: dictionary
        """

        # TODO slicing and check offset, length
        data_dictionary = {}
        for param in parameter:
            source_node = self._create_source_node(source)
            node = source_node + '/' + param

            # check if parameter exists
            if param in self._file[source_node].keys():
                data = self._file[node]['data']
                # TODO length
                data_mask = self._file[node]['mask']
                values = np.ma.masked_array(data, mask=data_mask)
                data_dictionary[param] = values
            elif param in self._file[source_node].attrs:
                data_dictionary[param] = self._file[source_node].attrs[param]
        return data_dictionary

    def write(self, source=None, data=[], configuration=None, offset=0, initial_size=1440):
        """Writes data to HDF5 file.
        
        :param source: The data source (device).
        :type source: string
        :param data: A list of recorded data (one dimensional dictionary) to be written.
        :type data: string list
        :param configuration: A two-dimensional dictionary for data configuration e.g. {'paramA':{type':'int8', 'attribute':False},...}
        :type configuration: dictionary 
        :param offset: offset to start writing data
        :type offset: integer
        :param initial_size: number of samples per day, the expected initial dataset size
        :type initial_size: integer
        :rtype: integer
        """
        
        # create source node if not exist
        source_node = self._create_source_node(source)
        
        # saving values to dataset
        for recording in data:
            for param, value in recording.items():
                
                node = source_node + '/' + param
                data_node = node + '/data'
                mask_node = node + '/mask'
                
                # write attribute
                # ---------------
                if configuration[param]['attribute'] == True:
                    # add attribute if not already exists
                    if param not in self._file[source_node].attrs:
                        self._file[source_node].attrs[param] = value
                        
                # write parameter
                # ---------------
                elif configuration[param]['attribute'] == False:
                    dataset_values = None
                    dataset_masked = None
                
                    if param not in self._file[source_node].keys():
                        dataset_values = self._file.create_dataset(data_node, (initial_size,), dtype=configuration[param]['type'])
                        dataset_masked = self._file.create_dataset(mask_node, (initial_size, 1), dtype=np.int8)
                        self._file[node].attrs['CLASS'] = 'GROUP'
                        self._file[node].attrs['TITLE'] = 'groupnode'
                        self._file[node].attrs['VERSION'] = '1.0' 
                        self._file[data_node].attrs['CLASS'] = 'ARRAY'
                        self._file[data_node].attrs['TITLE'] = 'data array'
                        self._file[data_node].attrs['VERSION'] = '2.4'
                        self._file[mask_node].attrs['CLASS'] = 'ARRAY'
                        self._file[mask_node].attrs['TITLE'] = 'mask array'
                        self._file[mask_node].attrs['VERSION'] = '2.4'
                    else:
                        dataset_values = self._file[data_node]
                        dataset_masked = self._file[mask_node]
                    
                    if value != None:
                        dataset_values[offset] = value
                        dataset_masked[offset] = 0
                # else: attribute == None
                 
            offset += 1
        return True
    
