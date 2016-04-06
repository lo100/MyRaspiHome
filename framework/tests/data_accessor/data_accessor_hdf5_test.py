import unittest
import sys
import logging
import numpy as np

from data_accessor.data_accessor_hdf5 import DataAccessorHDF5
# from data_accessor.exceptions import DataAccessorError

class TestDataAccessorHDF5(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)

    def test_new_data_accessor_hdf5(self):
        self.logger.info('test_new_data_accessor_hdf5: Create new data accessor HDF5.')
        da = DataAccessorHDF5()
        self.assertEqual(da.DATA_ACCESSOR_TYPE, 'hdf5')

    def test_write_read_hdf5(self):
        self.logger.info('test_write_read_hdf5: Open HDF5 file and write/read data to/from file.')
        da = DataAccessorHDF5()
        
        # write data to file
        da.open('C:\\Data\\wa\\MyRaspiHome\\output\\unittest.hdf5', 'w')
        configuration = {'float':{'type':'float32', 'attribute':False},
                        'integer':{'type':'int16', 'attribute':False},
                        'string':{'type':'S3', 'attribute':False},
                        'attr1':{'type':'int16', 'attribute':True},
                        'attr2':{'type':'S5', 'attribute':True}}
        recordings = []
        recordings.append({'float' : 0.1234,
                    'integer' : 1234,
                    'string' : 'abc'.encode('utf_8'),
                    'attr1' : '1234'.encode('utf_8'),
                    'attr2' : 'rec01'.encode('utf_8'),
                    })
        recordings.append({'float' : 0.5678,
                    'integer' : 5678,
                    'string' : 'def'.encode('utf_8'),
                    'attr1' : '2345'.encode('utf_8'),
                    'attr2' : 'rec02'.encode('utf_8'),
                    })
        
        da.write('unittest', recordings, configuration)
        da.close()
        
        # read data from file
        da.open('C:\\Data\\wa\\MyRaspiHome\\output\\unittest.hdf5', 'r')
        parameter = ('float', 'integer', 'string', 'attr1', 'attr2')
        data = da.read('unittest', parameter)
        self.assertEqual(data['float'][0], np.float32(recordings[0]['float']))
        self.assertEqual(data['integer'][0], recordings[0]['integer'])
        self.assertEqual(data['string'][0], recordings[0]['string'])
        self.assertEqual(data['float'][1], np.float32(recordings[1]['float']))
        self.assertEqual(data['integer'][1], recordings[1]['integer'])
        self.assertEqual(data['string'][1], recordings[1]['string'])        
        self.assertEqual(data['attr1'], recordings[0]['attr1'])
        self.assertEqual(data['attr2'], recordings[0]['attr2'])
        da.close()
                
        
    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()

