import unittest
import subprocess
from unittest.mock import patch
from internet_logger import InternetLogger

# python -m unittest internet_logger_tests.py
class TestInternetLogger(unittest.TestCase):

    def setUp(self):
        self.logger = InternetLogger()

    # Mock the output of the subprocess call to simulate a successful ping
    @patch('internet_logger.subprocess.check_output')
    def test_check_wifi_connection_connected(self, mock_check_output):
        mock_check_output.return_value = b"Ping successful"
        self.assertTrue(self.logger.check_wifi_connection())

    # Mock the subprocess call to raise a CalledProcessError to simulate a failed ping
    @patch('internet_logger.subprocess.check_output')
    def test_check_wifi_connection_disconnected(self, mock_check_output):
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'ping')
        self.assertFalse(self.logger.check_wifi_connection())

    # Test if the timestamp is in the correct format
    def test_get_current_timestamp(self):
        timestamp = self.logger.get_current_timestamp()
        self.assertRegex(timestamp, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

if __name__ == '__main__':
    unittest.main()