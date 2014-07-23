import unittest
import sys
import logging
from mock import patch

from data_mapper.data_mapper_interface import DataMapperInterface
from data_mapper.exceptions import DataMapperError

class TestDataMapper(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)

    def test_new_throws_exception(self):
        self.logger.info('test_new_throws_exception: Create undefined data mapper.')
        with self.assertRaises(DataMapperError) as context:
            DataMapperInterface('undefined')
        self.assertEqual(context.exception.message, 'Data mapper not implemented! undefined')

    @patch('data_mapper.data_mapper_tarom.DataMapperTarom')
    def test_new_data_mapper(self, mock_tarom):
        self.logger.info('test_new_data_mapper: Create new data mapper - mocked object.')
        mt = mock_tarom.return_value
        mt.MAPPER_TYPE = 'tarom'
        dmi = DataMapperInterface('tarom')
        dmi._mapper = mt
        self.assertEquals(dmi.get_type(), 'tarom')

    @patch('data_mapper.data_mapper_tarom.DataMapperTarom')
    def test_data_mapper_map(self, mock_tarom):
        self.logger.info('test_data_mapper_map: Call method map on mocked object.')
        mt = mock_tarom.return_value
        mt.map.return_value = {'key1' : 'value1', 'key2': 1, 'key3' : 1.0}
        dmi = DataMapperInterface('tarom')
        dmi._mapper = mt
        self.assertEquals(dmi.map('value1,value2,value3'), {'key1' : 'value1', 'key2': 1, 'key3' : 1.0})

    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()
