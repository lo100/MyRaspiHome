import unittest

from data_mapper.data_mapper_interface import DataMapperInterface
from data_mapper.exceptions import DataMapperError

class TestDataMapper(unittest.TestCase):
    
    def test_new_throws_exception(self):
        with self.assertRaises(DataMapperError) as context:
            dm = DataMapperInterface('undefined')
        self.assertEqual(context.exception.message, 'Data mapper not implemented! undefined')

    def test_new_tarom(self):
        dm = DataMapperInterface('tarom')
        self.assertEqual(dm.get_type(), 'tarom')
        
    # TODO: tests using mocks
