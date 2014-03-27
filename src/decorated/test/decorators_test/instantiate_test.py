# -*- coding: utf-8 -*-
from decorated.decorators.instantiate import Instantiate
from unittest2.case import TestCase
import inspect

class InstantiateTest(TestCase):
    def test_default_call(self):
        @Instantiate
        class Foo(object):
            def __call__(self, a, b):
                return a + b
        self.assertEquals('Foo', Foo.__name__)
        expected_module_name = 'decorated.test.decorators_test.instantiate_test'
        self.assertEquals(Foo.__module__, expected_module_name)
        self.assertTrue(inspect.isclass(Foo.class_))
        result = Foo(1, b=2)
        self.assertEqual(3, result)

    def test_custom_call(self):
        @Instantiate('run')
        class Foo(object):
            def run(self, a, b):
                return a + b
        result = Foo(1, b=2)
        self.assertEqual(3, result)

    def test_callable(self):
        @Instantiate('run')
        class Foo(object):
            def __call__(self, a, b):
                return a * b

            def run(self, a, b):
                return a + b
        result = Foo(1, b=2)
        self.assertEqual(3, result)
