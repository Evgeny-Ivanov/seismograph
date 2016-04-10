import unittest

from seismograph.exceptions import SeismographError


class SeismographErrorTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_exception_message(self):
        my_message = "my message"

        try:
            raise SeismographError(my_message)
        except SeismographError as e:
            e_message = e.message

        self.assertEqual(e_message, my_message)
