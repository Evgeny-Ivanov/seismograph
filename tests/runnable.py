# -*- coding: utf-8 -*-

import unittest
from seismograph.runnable import RunnableGroup
from seismograph.runnable import LayerOfRunnableObject
from seismograph.runnable import ContextOfRunnableObject
from mock import Mock,patch


class RunnableGroupTestCase(unittest.TestCase):
    def setUp(self):
        self.testStringConfig = "testString1"
        self.testStringObjects = "testString2"
        self.runnableGroup = RunnableGroup(self.testStringObjects,self.testStringConfig)

    def test_function__init__(self):
        self.assertEquals(self.runnableGroup._RunnableGroup__objects,self.testStringObjects)
        self.assertEquals(self.runnableGroup._RunnableGroup__config,self.testStringConfig)
        self.assertEquals(self.runnableGroup._is_run,False)

    def test_getPropertyConfig(self):
        self.assertEquals(self.runnableGroup.config,self.testStringConfig)

    def test_getPropertyObjects(self):
        self.assertEquals(self.runnableGroup.objects,self.testStringObjects)


class LayerOfRunnableObjectTestCase(unittest.TestCase):
    def test_function__init__(self):
        layerOfRunnableObject = LayerOfRunnableObject()
        self.assertEquals(layerOfRunnableObject.enabled,True)


class ContextOfRunnableObjectNotImplementedErrorTestCase(unittest.TestCase):
    def setUp(self):
        self.contextOfRunnableObject = ContextOfRunnableObject()

    def assertNotImplementedError(self,function,message):
        try:
            function()

            self.fail("NotImplementedError not raise")
        except NotImplementedError as e:
            self.assertEquals(e.message, '{} is not implemented in "{}"'
                              .format(message,self.contextOfRunnableObject.__class__.__name__, ))

    def test_getPropertyLayers(self):
        self.assertNotImplementedError(lambda :self.contextOfRunnableObject.layers,'Property "layers"')

    def test_getPropertyTeardown_callbacks(self):
        self.assertNotImplementedError(lambda: self.contextOfRunnableObject.teardown_callbacks, 'Property "teardown_callbacks"')

    def test_functionStart_context(self):
        self.assertNotImplementedError(lambda: self.contextOfRunnableObject.start_context(Mock()), 'Method "start_context"')

    def test_getPropertyStop_context(self):
        self.assertNotImplementedError(lambda: self.contextOfRunnableObject.stop_context(Mock()), 'Method "stop_context"')


class ContextOfRunnableObjectFunctionCallTestCase(unittest.TestCase):
    def setUp(self):
        self.contextOfRunnableObject = ContextOfRunnableObject()
        self.contextOfRunnableObject.start_context = Mock()
        self.contextOfRunnableObject.stop_context = Mock()
        self.testString = "testString"

    @patch("seismograph.runnable.stopped_on")
    def test_function___call___contextmanager(self,mock_runnable_stopped_on):
        mock_runnable_stopped_on.return_value = 'start_context'

        with self.contextOfRunnableObject(self.testString) as value:
            self.contextOfRunnableObject.start_context.assert_called_with(self.testString)
            self.assertFalse(mock_runnable_stopped_on.called)
            self.assertIsNone(value)

        mock_runnable_stopped_on.assert_called_with(self.testString)

    @patch("seismograph.runnable.stopped_on")
    def test_function___call___not_start_context(self, mock_runnable_stopped_on):
        mock_runnable_stopped_on.return_value = 'not start_context'

        with self.contextOfRunnableObject(self.testString) as value:
            pass

        self.contextOfRunnableObject.stop_context.assert_called_with(self.testString)

    @patch("seismograph.runnable.stopped_on")
    def test_function___call___start_context(self, mock_runnable_stopped_on):
        mock_runnable_stopped_on.return_value = 'start_context'

        with self.contextOfRunnableObject(self.testString) as value:
            pass

        self.assertFalse(self.contextOfRunnableObject.stop_context.called)