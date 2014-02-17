"""
   module:: data_mapper
   :synopsis: Data mapper for Steca Tarom solar charge controller.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

from data_mapper.exceptions import DataMapperError

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

    def map(self, data=None):
        """Returns data as a dictionary.
        
        :param data: data returned by charge controller
        :rtype: dictionary
        """
        position = 0
        dictionary = {}

        data.strip()
        data_array = data.split(';')

        # check if length equal protocol data array
        if len(data_array) != len(self.PROTOCOL_DATA):
            raise DataMapperError('Invalid data length, expected ' +
                                  str(len(self.PROTOCOL_DATA)) +
                                  ' got ' +
                                  str(len(data_array)) +
                                  ' data items!')

        for item in data_array:
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
            position += 1

        return dictionary


