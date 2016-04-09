import unittest

from seismograph.runnable import RunnableObject


class RunnableObjectTest(unittest.TestCase):
    def test_exception_smth(self):
        ro = RunnableObject()
        self.assertEqual(ro._stopped_on, 'run')


