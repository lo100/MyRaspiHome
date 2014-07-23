"""
   module:: data_accessor
   :synopsis: Wrapper class for data accessors.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

from data_accessor.exceptions import DataAccessorError
from data_accessor.data_accessor_hdf5 import DataAccessorHDF5

class DataAccessorInterface():

    """Data accessor instance.
    """
    _data_accessor = None

    def __init__(self, data_accessor):
        """Creates data accessor instance.
        
        :param data_accessor: The data accessor to be wrapped.
        :type data_accessor: string
        :raises: DataAccessorError
        """
        if data_accessor == 'hdf5':
            self._data_accessor = DataAccessorHDF5()
        else:
            raise DataAccessorError('Data accessor not implemented! ' +
                                    str(data_accessor))

    def get_type(self):
        """Returns the initialized data accessor type
        
        :rtype: string
        """
        return self._data_accessor.DATA_ACCESSOR_TYPE

    def open(self, filename, mode):
        """ Opens the file used by the data accessor.
        
        :param filename: Name of the file to be opened (including path).
        :type filename: string
        :param mode: File open mode
        :rtype: boolean
        """
        opened = False
        if self._data_accessor != None:
            self._data_accessor.open(filename)
            opened = True
        return opened

    def close(self):
        """ Closes the file used by the data accessor.
        
        :rtype: boolean
        """
        closed = False
        if self._data_accessor != None:
            self._data_accessor.close()
            closed = True
        return closed

    def read(self, *args):
        """Reads data from file.
        
        :param args: Depending on the data accessor implementation.
        :type args: multiple arguments
        :rtype: dictionary
        """
        data = None
        if self._data_accessor != None:
            data = self._data_accessor.read(args)
        return data

    def write(self, *args):
        """Writes data to file.
        
        :param args: Depending on the data accessor implementation.
        :type args: multiple arguments
        :rtype: integer
        """
        number_of_datasets = -1
        if self._data_accessor != None:
            number_of_datasets = self._data_accessor.write(args)
        return number_of_datasets

