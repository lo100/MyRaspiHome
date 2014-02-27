"""
   module:: data_mapper
   :synopsis: Data mapper for Steca Tarom solar charge controller.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

from data_mapper.exceptions import DataMapperError
from common.time import get_offset

class DataMapperTarom():

    """Mapper type.
    """
    MAPPER_TYPE = 'tarom'

    """Protocol data in series.
    """
    PROTOCOL_DATA = (
        'Version',
        'Date',
        'Time',
        'Battery Voltage',
        'Module Voltage 1',
        'Module Voltage 2',
        'State Of Charge',
        'State Of Health',
        'Total Battery Current',
        'Max Input Current Module 1',
        'Max Input Current Module 2',
        'Module Input Current',
        'Total Charge Current',
        'Device Load Current',
        'Total Current',
        'Temperature Battery Sensor',
        'Error Status',
        'Charging Mode',
        'Load Switch',
        'Auxiliary 1',
        'Auxiliary 2',
        'Max Ah Battery 24 Hours',
        'Total Ah Battery',
        'Max Ah Load 24 Hours',
        'Total Ah Load',
        'Derating',
        'Checksum',
    )

    """The frequency / sample rate.
    One sample per minute.
    """
    FREQUENCY = 0.0166666666666667

    def __init__(self):
        pass

    def _is_float(self, value):
        _float = False
        try:
            float(value)
            _float = True
        except (TypeError, ValueError):
            pass
        return _float

    def _is_integer(self, value):
        _integer = False
        try:
            int(value)
            _integer = True
        except (TypeError, ValueError):
            pass
        return _integer

    def _map_single_recording(self, data=None):
        """Returns data as a dictionary.
        
        :param data: data returned by charge controller
        :type data: data string with EOL
        :rtype: dictionary
        """
        data.strip()
        data_array = data.split(';')

        # check if length equal protocol data array
        if len(data_array) != len(self.PROTOCOL_DATA):
            raise DataMapperError('Invalid data length, expected ' +
                                  str(len(self.PROTOCOL_DATA)) +
                                  ' got ' +
                                  str(len(data_array)) +
                                  ' data items!')

        dictionary = {}
        dictionary['FREQUENCY'] = self.FREQUENCY
        dictionary['OFFSET'] = get_offset(data_array[2] + ':00', self.FREQUENCY)

        for position, item in enumerate(data_array, start=0):
            value = None
            if item != '#':
                # special handling for checksum - can be string or integer
                if position == (len(self.PROTOCOL_DATA) - 1):
                    value = item
                elif self._is_integer(item):
                    value = int(item)
                elif self._is_float(item):
                    value = float(item)
                else:
                    value = item

            dictionary[self.PROTOCOL_DATA[position]] = value

        return dictionary

    def map(self, data=None):
        """Returns data as a list of dictionaries.
        
        A single dictionary must contain the following keys:
        FREQUENCY : The frequency / sample rate.
        OFFSET : The dataset offset (index) for the recording starting from midnight
            e.g. 07:00:00 --> 1 Hz sample rate
                 --> (7 (hours) * 60 (minutes) * 60 (seconds)) * 1 (frequency)
                 ==> 25200
        
        :param data: list of data returned by charge controller
        :type data: list of strings
        :rtype: list of dictionaries
        """
        dictionaries = []

        for recording in data:
            dictionary = self._map_single_recording(recording)
            dictionaries.append(dictionary)

        return dictionaries




