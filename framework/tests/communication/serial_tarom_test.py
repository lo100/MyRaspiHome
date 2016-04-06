import unittest
import sys
import logging
from unittest.mock import patch

from communication.serial_interface import SerialTarom
from communication.exceptions import SerialConnectionError

class TestSerialTarom(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)

    def test_new_serial_tarom(self):
        self.logger.info('test_new_serial_tarom: Create serial interface for Steca Tarom.')
        st = SerialTarom()
        self.assertEqual(st.INTERFACE_TYPE, 'tarom')

    @patch('serial.Serial')
    def test_open_tarom(self, mock_serial):
        self.logger.info('test_open_tarom: Call method open on mocked object.')
        ms = mock_serial.return_value
        ms.open.return_value = True
        st = SerialTarom()
        st._serial = ms
        self.assertTrue(st.open())

    @patch('serial.Serial')
    def test_open_tarom_raises_exception(self, mock_serial):
        self.logger.info('test_open_tarom_raises_exception: Call method open on mocked object and raise SerialConnectionError exception.')
        ms = mock_serial.side_effect = SerialConnectionError
        st = SerialTarom()
        st._serial = ms
        with self.assertRaises(SerialConnectionError):
            st.open()

    @patch('serial.Serial')
    def test_close_tarom(self, mock_serial):
        self.logger.info('test_close_tarom: Call method close on mocked object.')
        ms = mock_serial.return_value
        ms.close.return_value = True
        st = SerialTarom()
        st._serial = ms
        self.assertTrue(st.close())

    @patch('serial.Serial')
    def test_read_tarom(self, mock_serial):
        self.logger.info('test_read_tarom: Call method read on mocked object.')
        ms = mock_serial.return_value
        ms.readline.return_value = 'Serial.readline()'
        st = SerialTarom()
        st._serial = ms
        self.assertEquals(st.read(), 'Serial.readline()')

    @patch('serial.Serial')
    def test_write_tarom(self, mock_serial):
        self.logger.info('test_write_tarom: Call method write on mocked object.')
        ms = mock_serial.return_value
        ms.write.return_value = 19
        st = SerialTarom()
        st._serial = ms
        self.assertEquals(st.write('SerialTarom.write()'), 19)

    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()
