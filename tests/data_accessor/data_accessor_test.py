import unittest
import sys
import logging
from mock import patch

from data_accessor.data_accessor_interface import DataAccessorInterface
from data_accessor.exceptions import DataAccessorError

class TestDataAccessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)

    def test_new_throws_exception(self):
        self.logger.info('test_new_throws_exception: Create undefined data accessor interface.')
        with self.assertRaises(DataAccessorError) as context:
            DataAccessorInterface('undefined')
        self.assertEqual(context.exception.message, 'Data accessor not implemented! undefined')

    @patch('data_accessor.data_accessor_hdf5.DataAccessorHDF5')
    def test_new_data_accessor(self, mock_hdf5):
        self.logger.info('test_new_data_accessor: Create new data accessor interface.')
        da = DataAccessorInterface('hdf5')
        self.assertEqual(da.get_type(), 'hdf5')

    @patch('data_accessor.data_accessor_hdf5.DataAccessorHDF5')
    def test_get_type_data_accessor(self, mock_hdf5):
        self.logger.info('test_get_type_data_accessor: Call method get_type on mocked object.')
        mh = mock_hdf5.return_value
        mh.DATA_ACCESSOR_TYPE = 'hdf5'
        dai = DataAccessorInterface('hdf5')
        dai._data_accessor = mh
        self.assertEquals(dai.get_type(), 'hdf5')

    @patch('data_accessor.data_accessor_hdf5.DataAccessorHDF5')
    def test_open_data_accessor(self, mock_hdf5):
        self.logger.info('test_open_data_accessor: Call method open on mocked object.')
        mh = mock_hdf5.return_value
        mh.open.return_value = True
        dai = DataAccessorInterface('hdf5')
        dai._data_accessor = mh
        self.assertTrue(dai.open('test.hdf5', 'r'))

    @patch('data_accessor.data_accessor_hdf5.DataAccessorHDF5')
    def test_close_data_accessor(self, mock_hdf5):
        self.logger.info('test_close_data_accessor: Call method close on mocked object.')
        mh = mock_hdf5.return_value
        mh.close.return_value = True
        dai = DataAccessorInterface('hdf5')
        dai._data_accessor = mh
        self.assertTrue(dai.close())

    @patch('data_accessor.data_accessor_hdf5.DataAccessorHDF5')
    def test_read_data_accessor(self, mock_hdf5):
        self.logger.info('test_read_data_accessor: Call method read on mocked object.')
        mh = mock_hdf5.return_value
        values = {'value': 1}
        mh.read.return_value = values
        dai = DataAccessorInterface('hdf5')
        dai._data_accessor = mh
        self.assertEquals(dai.read(10, 1), {'value': 1})

    @patch('data_accessor.data_accessor_hdf5.DataAccessorHDF5')
    def test_write_data_accessor(self, mock_hdf5):
        self.logger.info('test_write_data_accessor: Call method write on mocked object.')
        mh = mock_hdf5.return_value
        mh.write.return_value = 1
        dai = DataAccessorInterface('hdf5')
        dai._data_accessor = mh
        data = {'value': 1}
        self.assertEquals(dai.write(data, 10, 1), 1)

    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()

