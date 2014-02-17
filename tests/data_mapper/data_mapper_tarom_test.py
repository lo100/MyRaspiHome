import unittest
import sys
import logging

from data_mapper.data_mapper_interface import DataMapperInterface
from data_mapper.exceptions import DataMapperError

class TestDataMapperTarom(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)

    def test_new_tarom(self):
        self.logger.info('test_new_tarom: Create Steca Tarom data mapper.')
        dm = DataMapperInterface('tarom')
        self.assertEqual(dm.get_type(), 'tarom')

    def test_map_tarom(self):
        self.logger.info('test_map_tarom: Test mapping function of Steca Tarom data mapper.')
        dm = DataMapperInterface('tarom')
        actual = dm.map('1;2014/02/06;13:40;13.0;13.7;#;99.0;#;2.0;2.0;#;2.0;2.0;0.0;0.0;19.3;0;B;1;1;0;3.2;579.2;0.0;72.0;0;5679')
        expected = {'Version' : 1,
                    'Date' : '2014/02/06',
                    'Time' : '13:40',
                    'Battery Voltage' : 13.0,
                    'Module Voltage 1' : 13.7,
                    'Module Voltage 2' : None,
                    'State Of Charge' : 99.0,
                    'State Of Health': None,
                    'Total Battery Current' : 2.0,
                    'Max Input Current Module 1' : 2.0,
                    'Max Input Current Module 2' : None,
                    'Module Input Current' : 2.0,
                    'Total Charge Current' : 2.0,
                    'Device Load Current' : 0.0,
                    'Total Current' : 0.0,
                    'Temperature Battery Sensor' : 19.3,
                    'Error Status': 0,
                    'Charging Mode' : 'B',
                    'Load Switch' : 1,
                    'Auxiliary 1' : 1,
                    'Auxiliary 2' : 0,
                    'Max Ah Battery 24 Hours': 3.2,
                    'Total Ah Battery' : 579.2,
                    'Max Ah Load 24 Hours' : 0.0,
                    'Total Ah Load' : 72.0,
                    'Derating' : 0,
                    'Checksum' : '5679',
                    }
        self.assertEqual(actual, expected)

    def test_map_tarom_invalid_size(self):
        self.logger.info('test_map_tarom_invalid_size: Test mapping function of Steca Tarom data mapper with invalid length of data.')
        with self.assertRaises(DataMapperError) as context:
            dm = DataMapperInterface('tarom')
            dm.map('1;2014/02/06;13:40')
        self.assertEqual(context.exception.message, 'Invalid data length, expected 27 got 3 data items!')

    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()


