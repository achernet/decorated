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
        self.assertEqual('Foo', Foo.__name__)
        potential_namespace_parts = ["decorators_test", "test", "decorated"]
        potential_namespaces = ["instantiate_test"]
        for ns_part in reversed(potential_namespace_parts):
            potential_namespaces.append(".".join([ns_part, potential_namespaces[-1]]))
        self.assertIn(Foo.__module__, potential_namespaces)
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
