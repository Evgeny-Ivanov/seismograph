import unittest
from seismograph.datastructures import Context


class TestDatastructures(unittest.TestCase):
    def setUp(self):
        self.context = Context()
        self.itemTest = 0

    def test_setattr(self):
        testString = "hello world"
        self.context.__setattr__(self.itemTest,testString)
        self.assertEqual(self.context[self.itemTest], testString)

    def test_getattr_raise_AttributeError(self):
        self.assertRaises(AttributeError,self.context.__getattr__,self.itemTest)

    def test_getattr_AttributeError_message(self):
        className = "Context"
        testString = '"{}" does not have "{}" attribute.'.format(className, self.itemTest)

        try:
            self.context.__delattr__(self.itemTest)
        except AttributeError as e:
            self.assertEquals(e.message, testString)

    def test_delattr_del(self):
        self.context[self.itemTest] = 11
        self.context.__delattr__(self.itemTest)
        self.assertRaises(AttributeError,self.context.__getattr__,self.itemTest)

    def test_delattr_raise_AttributeError(self):
        self.assertRaises(AttributeError,self.context.__delattr__,self.itemTest)

    def test_delattr_AttributeError_message(self):
        self.context[self.itemTest] = "testString"
        self.context.__delattr__(self.itemTest)
        self.assertRaises(AttributeError,self.context.__getattr__,self.itemTest)

    def test_copy(self):
        self.context[0] = "hello"
        self.context[1] = "world"

        newContext = self.context.copy()
        self.assertEquals(self.context,newContext)

    def tearDown(self):
        pass
