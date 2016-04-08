# -*- coding: utf-8 -*-

import unittest
from mock import Mock
from seismograph.ext import mocker
from seismograph import extensions
from seismograph.extensions import set,get
from seismograph.extensions import install
from seismograph.extensions import add_options
from seismograph.extensions import ExtensionContainer,SingletonExtensionContainer
from seismograph.program import Program
from seismograph import config

class TestExtensions(unittest.TestCase):
    def setUp(self):
        self.testString = "testString"
        self.testItem = 0

        self._WAS_CLEAR = extensions._WAS_CLEAR

    def test_functionInstall(self):
        mocker.__install__ = Mock()
        program = Program()
        install(mocker,program)

        mocker.__install__.assert_called_with(program)

    def test_functionAdd_options(self):
        mocker.__add_options__ = Mock()
        parser = config.create_option_parser()
        add_options(mocker,parser)
        mocker.__add_options__.assert_called_with(parser)

    def test_classExtensionContainer_get_properties(self):
        ext = self.testString
        args = tuple()
        kwargs = dict()
        extensionContainer = ExtensionContainer(ext=ext,args=args,kwargs=kwargs)
        self.assertEquals(extensionContainer.ext,ext)
        self.assertEquals(extensionContainer.args,args)
        self.assertEquals(extensionContainer.kwargs,kwargs)

    def test_ExtensionContainer___call__(self):
        extensionContainer = ExtensionContainer(ext=lambda  : self.testString)
        self.assertEquals(self.testString,extensionContainer())

    def test_SingletonExtensionContainer___call__(self):
        extensionContainer = SingletonExtensionContainer(ext=lambda  : self.testString)
        self.assertEquals(self.testString, extensionContainer())

    def test_functionSet_is_data_True(self):
        set(ext=self.testString,name=self.testString,is_data=True,singleton=False)
        self.assertEquals(extensions._TMP[self.testString],self.testString)

    def test_functionSet_is_data_False_singleton_True(self):
        set(ext=self.testString,name=self.testString,is_data=False,singleton=True)
        self.assertIsInstance(extensions._TMP[self.testString],SingletonExtensionContainer)

    def test_functionSet_is_data_False_singleton_False(self):
        set(ext=self.testString,name=self.testString,is_data=False,singleton=False)
        self.assertIsInstance(extensions._TMP[self.testString],ExtensionContainer)
        self.assertNotIsInstance(extensions._TMP[self.testString],SingletonExtensionContainer)


    def test_functionClear(self):
        extensions._WAS_CLEAR = False

        extensions.clear()
        self.assertEquals(extensions._TMP,{})
        self.assertEquals(extensions._WAS_CLEAR,True)

    def test_functionGet_raiseExtensionNotFound(self):
        extensions._WAS_CLEAR = False
        self.assertRaises(extensions.ExtensionNotFound,get,self.testItem)

    def test_functionGet_raiseRuntimeError(self):
        extensions._WAS_CLEAR = True
        self.assertRaises(RuntimeError,get,self.testItem)

    def test_functionGet_InstanceExtensionContainer(self):
        class TestMock(Mock,ExtensionContainer):
            pass
        mock = TestMock(Mock())
        mock.return_value = self.testString

        extensions._TMP[self.testItem] = mock
        self.assertEquals(self.testString, get(self.testItem))
        self.assertTrue(mock.called)

    def tearDown(self):
        extensions._TMP.clear();
        extensions._WAS_CLEAR = self._WAS_CLEAR



