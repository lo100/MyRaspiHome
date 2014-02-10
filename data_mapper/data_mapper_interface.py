"""
   module:: data_mapper
   :synopsis: Wrapper class for data mapper.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

from data_mapper.exceptions import DataMapperError
from data_mapper.data_mapper_tarom import DataMapperTarom

class DataMapperInterface():

    """Data mapper instance.
    """
    _mapper = None
    
    def __init__(self, mapper):
        """Creates a wrapped data mapper instance.
        
        :param mapper: The mapper to be wrapped.
        :type interface: string
        :raises: DataMapperError
        """
        if mapper == 'tarom':
            self._mapper = DataMapperTarom()
        else:
            raise DataMapperError('Data mapper not implemented! ' + 
                                        str(mapper))
        
    def get_type(self):
        """Returns the data mapper type.
        
        :rtype: string
        """
        return self._mapper.MAPPER_TYPE
    
    def map(self, data=None):
        """Returns data as a dictionary.
        
        :param data: data returned by devices
        :rtype: dictionary
        """
        return self._mapper.map(data)
    
