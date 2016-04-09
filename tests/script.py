# -*- coding: utf-8 -*-

import unittest
from mock import Mock
from seismograph.script import Script

class ScriptTestCase(unittest.TestCase):
    def setUp(self):
        self.testString = "testString"

    def test_class_script_get_property_config(self):
        mock = Mock()
        script = Script(mock)
        mock.config = self.testString
        self.assertEquals(script.config,self.testString)
