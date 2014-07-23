import unittest
import sys
import logging

from common.time import get_offset

class TestTime(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)

    def test_get_offset(self):
        self.logger.info('test_get_offset: Calculate offsets using various frequencies.')
        offset = get_offset('00:00:00', 1)
        self.assertEqual(0, offset)
        offset = get_offset('07:00:00')
        self.assertEqual(25200, offset)
        offset = get_offset('23:59:59', 1)
        self.assertEqual(86399, offset)
        offset = get_offset('07:00:00', 0.0166666666666667)
        self.assertEqual(420, offset)
        offset = get_offset('07:00:00', 0.5)
        self.assertEqual(12600, offset)

    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()
