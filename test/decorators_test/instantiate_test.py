# -*- coding: utf-8 -*-
from decorated.decorators.instantiate import Instantiate
from unittest.case import TestCase

class InstantiateTest(TestCase):
    def test_default_call(self):
        @Instantiate
        class Foo(object):
            def __call__(self, a, b):
                return a + b
        result = Foo(1, b=2)
        self.assertEqual(3, result)
        
    def test_custom_call(self):
        @Instantiate('run')
        class Foo(object):
            def run(self, a, b):
                return a + b
        result = Foo(1, b=2)
        self.assertEqual(3, result)
        