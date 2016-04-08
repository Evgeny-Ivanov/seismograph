import unittest
from mock import Mock
from seismograph.script import Script

class TestScript(unittest.TestCase):
    def setUp(self):
        self.testString = "testString"

    def test_classScript_getPropertyConfig(self):
        mock = Mock()
        script = Script(mock)
        mock.config = self.testString
        self.assertEquals(script.config,self.testString)
