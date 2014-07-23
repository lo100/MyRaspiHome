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
        """Returns data as a list of dictionaries.
        
        A single dictionary must contain the following keys:
        FREQUENCY : The frequency / sample rate.
        OFFSET : The dataset offset (index) for the recording starting from midnight
            e.g. 07:00:00 --> 1 Hz sample rate
                 --> (7 (hours) * 60 (minutes) * 60 (seconds)) * 1 (frequency)
                 ==> 25200
        
        :param data: data returned by devices
        :type data: list of strings (data recordings)
        :rtype: dictionary
        """
        return self._mapper.map(data)

