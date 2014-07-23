import unittest
import sys
import logging
from mock import patch

from communication.serial_interface import SerialInterface
from communication.exceptions import SerialConnectionError

logger = logging.getLogger()
logger.level = logging.DEBUG

class TestSerialInterface(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)

    def test_new_throws_exception(self):
        self.logger.info('test_new_throws_exception: Create undefined serial interface.')
        with self.assertRaises(SerialConnectionError) as context:
            SerialInterface('undefined')
        self.assertEqual(context.exception.message, 'Serial interface not implemented! undefined')

    @patch('communication.serial_tarom.SerialTarom')
    def test_get_type_serial_interface(self, mock_tarom):
        self.logger.info('test_get_type_serial_interface: Call method get_type on mocked object.')
        mt = mock_tarom.return_value
        mt.INTERFACE_TYPE = 'tarom'
        si = SerialInterface('tarom')
        si._interface = mt
        self.assertEquals(si.get_type(), 'tarom')

    @patch('communication.serial_tarom.SerialTarom')
    def test_open_serial_interface(self, mock_tarom):
        self.logger.info('test_open_serial_interface: Call method open on mocked object.')
        mt = mock_tarom.return_value
        mt.open.return_value = True
        si = SerialInterface('tarom')
        si._interface = mt
        self.assertTrue(si.open())

    @patch('communication.serial_tarom.SerialTarom')
    def test_close_serial_interface(self, mock_tarom):
        self.logger.info('test_close_serial_interface: Call method close on mocked object.')
        mt = mock_tarom.return_value
        mt.close.return_value = True
        si = SerialInterface('tarom')
        si._interface = mt
        self.assertTrue(si.close())

    @patch('communication.serial_tarom.SerialTarom')
    def test_read_serial_interface(self, mock_tarom):
        self.logger.info('test_read_serial_interface: Call method read on mocked object.')
        mt = mock_tarom.return_value
        mt.read.return_value = 'SerialTarom.read()'
        si = SerialInterface('tarom')
        si._interface = mt
        self.assertEquals(si.read(), 'SerialTarom.read()')

    @patch('communication.serial_tarom.SerialTarom')
    def test_write_serial_interface(self, mock_tarom):
        self.logger.info('test_write_serial_interface: Call method write on mocked object.')
        mt = mock_tarom.return_value
        mt.write.return_value = 24
        si = SerialInterface('tarom')
        si._interface = mt
        self.assertEquals(si.write(), 24)

    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()
