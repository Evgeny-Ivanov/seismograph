import unittest

from seismograph.runnable import RunnableGroup, RunnableObject, stopped_on, reason, is_run, run, BuildObjectMixin, \
    is_mount, MountObjectMixin, is_build, run_method, mount_method, build_method
from seismograph.runnable import LayerOfRunnableObject
from seismograph.runnable import ContextOfRunnableObject
from mock import Mock


def assertNotImplementedError(self, function, message, class_name):
    try:
        function()

        self.fail("NotImplementedError not raise")
    except NotImplementedError as e:
        self.assertEquals(e.message, '{} is not implemented in "{}"'
                          .format(message, class_name))


class TestClassRunnableGroup(unittest.TestCase):
    def setUp(self):
        self.testStringConfig = "testString1"
        self.testStringObjects = "testString2"
        self.runnableGroup = RunnableGroup(self.testStringObjects, self.testStringConfig)

    def test_function__init__(self):
        self.assertEquals(self.runnableGroup._RunnableGroup__objects, self.testStringObjects)
        self.assertEquals(self.runnableGroup._RunnableGroup__config, self.testStringConfig)
        self.assertEquals(self.runnableGroup._is_run, False)

    def test_getPropertyConfig(self):
        self.assertEquals(self.runnableGroup.config, self.testStringConfig)

    def test_getPropertyObjects(self):
        self.assertEquals(self.runnableGroup.objects, self.testStringObjects)


class TestClassLayerOfRunnableObject(unittest.TestCase):
    def test_function__init__(self):
        layerOfRunnableObject = LayerOfRunnableObject()
        self.assertEquals(layerOfRunnableObject.enabled, True)


class TestContextOfRunnableObject(unittest.TestCase):
    def setUp(self):
        self.contextOfRunnableObject = ContextOfRunnableObject()

    def test_getPropertyLayers(self):
        assertNotImplementedError(self, lambda: self.contextOfRunnableObject.layers,
                                  'Property "layers"',
                                  self.contextOfRunnableObject.__class__.__name__)

    def test_getPropertyTeardown_callbacks(self):
        assertNotImplementedError(self, lambda: self.contextOfRunnableObject.teardown_callbacks,
                                  'Property "teardown_callbacks"',
                                  self.contextOfRunnableObject.__class__.__name__)

    def test_functionStart_context(self):
        assertNotImplementedError(self, lambda: self.contextOfRunnableObject.start_context(Mock()),
                                  'Method "start_context"',
                                  self.contextOfRunnableObject.__class__.__name__)

    def test_getPropertyStop_context(self):
        assertNotImplementedError(self, lambda: self.contextOfRunnableObject.stop_context(Mock()),
                                  'Method "stop_context"',
                                  self.contextOfRunnableObject.__class__.__name__)


class TestRunnablePy(unittest.TestCase):
    def setUp(self):
        self.testString = "testString"
        self.RunnableObject = RunnableObject()

    def test_stopped_on(self):
        self.assertEqual(stopped_on(self.RunnableObject), "run")

    def test_stopped_on2(self):
        self.assertEqual(stopped_on(self.RunnableObject, self.testString), self.testString)

    def test_reason(self):
        self.assertEqual(reason(self.RunnableObject),
                         'Your reason can be here. This is from "{}.{}.__reason__" method.\n'.format(
                             self.RunnableObject.__class__.__module__, self.RunnableObject.__class__.__name__, ))

    def ignore_test_is_run(self):
        assertNotImplementedError(self, lambda: is_run(self.RunnableObject),
                                  'Method "__is_run__"',
                                  self.RunnableObject.__class__.__name__)

    def ignore_test_run(self):
        assertNotImplementedError(self, lambda: run(self.RunnableObject, Mock(), Mock()),
                                  'Method "run"',
                                  self.RunnableObject.__class__.__name__)

    def test_is_mount_1(self):
        try:
            is_mount(MountObjectMixin())
        except AssertionError:
            self.fail("AssertionError")
        except NotImplementedError:
            pass

    def test_is_mount_2(self):
        try:
            is_mount(object())
        except AssertionError:
            pass
        except NotImplementedError:
            pass
        else:
            self.fail("No AssertionError")

    def test_is_build_1(self):
        try:
            is_build(BuildObjectMixin())
        except AssertionError:
            self.fail("AssertionError")
        except NotImplementedError:
            pass

    def test_is_build_2(self):
        try:
            is_build(object())
        except AssertionError:
            pass
        except NotImplementedError:
            pass
        else:
            self.fail("No AssertionError")


class TestRunnablePy_run_method(unittest.TestCase):
    def setUp(self):
        self.RunnableObject = RunnableObject()

    @staticmethod
    @run_method
    def example(obj):
        pass

    def test_run_method1(self):
        mock = Mock()
        mock.__is_run__ = lambda: True
        self.example(mock)

    def test_run_method2(self):
        mock = Mock()
        mock.__is_run__ = lambda: False

        try:
            self.example(mock)
        except AssertionError:
            pass
        else:
            self.fail("No AssertionError")


class TestRunnablePy_mount_method(unittest.TestCase):
    def setUp(self):
        self.RunnableObject = RunnableObject()

    @staticmethod
    @mount_method
    def example(obj):
        pass

    def test_mount_method1(self):
        mock = Mock(spec=MountObjectMixin)
        mock.__is_mount__ = lambda: True
        self.example(mock)

    def test_mount_method2(self):
        mock = Mock()
        mock.__is_mount__ = lambda: False

        f = False
        try:
            self.example(mock)
        except AssertionError:
            f = True

        self.assertTrue(f)


class TestRunnablePy_build_method(unittest.TestCase):
    @staticmethod
    @build_method
    def example(obj):
        pass

    def test_build_method1(self):
        mock = Mock(spec=BuildObjectMixin)
        mock.__is_build__ = lambda: True
        self.example(mock)

    def test_build_method2(self):
        mock = Mock()
        mock.__is_build__ = lambda: False

        f = False
        try:
            self.example(mock)
        except AssertionError:
            f = True

        self.assertTrue(f)


class TestClassRunnableObject(unittest.TestCase):
    def setUp(self):
        self.testString = "testString"
        self.RunnableObject = RunnableObject()

    def test_getPropertyId(self):
        self.assertGreater(self.RunnableObject.id, 0)

    def test_support_mp(self):
        mock = Mock()
        mock.Value = lambda _1, _2: self.testString
        self.RunnableObject.support_mp(mock)
        self.assertEqual(self.RunnableObject._stopped_on, self.testString)
