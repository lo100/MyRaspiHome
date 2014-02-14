import unittest

from serial.serial_interface import SerialInterface
from serial.exceptions import SerialConnectionError

class TestSerialInterface(unittest.TestCase):
    
    def test_new_throws_exception(self):
        with self.assertRaises(SerialConnectionError) as context:
            serial = SerialInterface('undefined')
        self.assertEqual(context.exception.message, 'Serial interface not implemented! undefined')

    def test_new_tarom(self):
        serial = SerialInterface('tarom')
        self.assertEqual(serial.get_type(), 'tarom')
        
    # TODO: tests using mocks
