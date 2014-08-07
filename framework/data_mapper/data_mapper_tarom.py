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

    """Protocol data in order.
    """
    PROTOCOL_DATA = (
        'Version',
        'Date',
        'Time',
        'Battery_Voltage',
        'Module_Voltage_1',
        'Module_Voltage_2',
        'State_Of_Charge',
        'State_Of_Health',
        'Total_Battery_Current',
        'Max_Input_Current_Module_1',
        'Max_Input_Current_Module_2',
        'Module_Input_Current',
        'Total_Charge_Current',
        'Device_Load_Current',
        'Total_Current',
        'Temperature_Battery_Sensor',
        'Error_Status',
        'Charging_Mode',
        'Load_Switch',
        'Auxiliary_1',
        'Auxiliary_2',
        'Max_Ah_Battery_24_Hours',
        'Total_Ah_Battery',
        'Max_Ah_Load_24_Hours',
        'Total_Ah_Load',
        'Derating',
        'Checksum',
    )

    """Data configuration.
    """
    DATA_CONFIGURATION = {
        'FREQUENCY':{'type':'float64', 'attribute':True},
        'OFFSET':{'type':'int16', 'attribute':True},
        'Version':{'type':'int8', 'attribute':True},
        'Date':{'type':'S10', 'attribute':True},
        'Time':{'type':'S5', 'attribute':None},
        'Battery_Voltage':{'type':'float32', 'attribute':False},
        'Module_Voltage_1':{'type':'float32', 'attribute':False},
        'Module_Voltage_2':{'type':'float32', 'attribute':False},
        'State_Of_Charge':{'type':'float32', 'attribute':False},
        'State_Of_Health':{'type':'float32', 'attribute':False},
        'Total_Battery_Current':{'type':'float32', 'attribute':False},
        'Max_Input_Current_Module_1':{'type':'float32', 'attribute':False},
        'Max_Input_Current_Module_2':{'type':'float32', 'attribute':False},
        'Module_Input_Current':{'type':'float32', 'attribute':False},
        'Total_Charge_Current':{'type':'float32', 'attribute':False},
        'Device_Load_Current':{'type':'float32', 'attribute':False},
        'Total_Current':{'type':'float32', 'attribute':False},
        'Temperature_Battery_Sensor':{'type':'float32', 'attribute':False},
        'Error_Status':{'type':'int8', 'attribute':False},
        'Charging_Mode':{'type':'S3', 'attribute':False},
        'Load_Switch':{'type':'int8', 'attribute':False},
        'Auxiliary_1':{'type':'int8', 'attribute':False},
        'Auxiliary_2':{'type':'int8', 'attribute':False},
        'Max_Ah_Battery_24_Hours':{'type':'float32', 'attribute':False},
        'Total_Ah_Battery':{'type':'float32', 'attribute':False},
        'Max_Ah_Load_24_Hours':{'type':'float32', 'attribute':False},
        'Total_Ah_Load':{'type':'float32', 'attribute':False},
        'Derating':{'type':'int8', 'attribute':False},
        'Checksum':{'type':'S4', 'attribute':False},
    }
    
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




