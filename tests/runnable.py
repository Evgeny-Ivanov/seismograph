import unittest
from seismograph.runnable import RunnableGroup
from seismograph.runnable import LayerOfRunnableObject
from seismograph.runnable import ContextOfRunnableObject
from mock import Mock


class TestClassRunnableGroup(unittest.TestCase):
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


class TestClassLayerOfRunnableObject(unittest.TestCase):
    def test_function__init__(self):
        layerOfRunnableObject = LayerOfRunnableObject()
        self.assertEquals(layerOfRunnableObject.enabled,True)


class TestContextOfRunnableObject(unittest.TestCase):
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


