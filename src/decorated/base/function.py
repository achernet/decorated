# -*- coding: UTF-8 -*-
from decorated.base.proxy import Proxy
from decorated.util import templates
from weakref import WeakKeyDictionary
import doctest
import functools
import inspect

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__', '__code__', 'func_code')

class Function(Proxy):

    def __init__(self, *args, **kw):
        super(Function, self).__init__()
        self.params = None
        self.required_params = None
        self.optional_params = None
        self._decorate_or_call = self._decorate
        self._static_cache = {}
        self._instance_cache = WeakKeyDictionary()
        if len(args) == 1 and callable(args[0]) and len(kw) == 0:
            self._init()
            self._decorate(args[0])
        else:
            self._init(*args, **kw)

    def __call__(self, *args, **kw):
        return self._decorate_or_call(*args, **kw)

    def __get__(self, obj, cls):
        cache = self._static_cache if obj is None else self._instance_cache
        key = obj or cls
        cached = cache.get(key)
        if cached is not None:
            return cached
        call_args = (obj,) if obj is not None else ()
        method = partial(Function, call_args=call_args)(self)
        method.im_class = cls
        method.im_func = method.__func__ = self
        method.im_self = method.__self__ = obj
        cache[key] = method
        return method

    def __str__(self):
        return '<Function %s.%s>' % (self._func.__module__, self.__name__)

    def target(self):
        return self._func.target() if isinstance(self._func, Function) else self._func

    def _call(self, *args, **kw):
        return self._func(*args, **kw)

    def _compile_template(self, template):
        return templates.compile(template, self.params)

    def _decorate(self, func):
        self._func = func
        functools.update_wrapper(self, func, WRAPPER_ASSIGNMENTS, updated=())
        if isinstance(func, Function):
            self.params = func.params
            self.required_params = func.required_params
            self.optional_params = func.optional_params
        else:
            self._parse_params(func)
        self._decorate_or_call = self._call
        return self

    def _evaluate_expression(self, expression, *args, **kw):
        d = self._resolve_args(*args, **kw)
        return eval(expression, d)

    def _init(self, *args, **kw):
        pass

    def _parse_params(self, func):
        self.params, _, _, defaults = inspect.getargspec(func)
        if defaults:
            self.required_params = self.params[:-len(defaults)]
            self.optional_params = []
            for i in range(len(defaults) - 1, -1, -1):
                self.optional_params.append((self.params[-1 - i], defaults[-1 - i]))
        else:
            self.required_params = self.params
            self.optional_params = ()
        if _is_bound_method(func):
            self.params = self.params[1:]
            self.required_params = self.required_params[1:]
        self.params = tuple(self.params)
        self.required_params = tuple(self.required_params)
        self.optional_params = tuple(self.optional_params)

    def _resolve_args(self, *args, **kw):
        d = dict([(name, default) for name, default in self.optional_params])
        for param, arg in zip(self.params, args):
            d[param] = arg
        d.update(kw)
        for name in self.params:
            if name not in d:
                raise Exception('Missing argument "%s" for %s.' % (name, str(self)))
        d = dict([(k, v) for k, v in d.items() if k in self.params])
        return d

    def _target(self):
        return self._func

def partial(func, init_args=(), init_kw=None, call_args=(), call_kw=None):
    if init_kw is None:
        init_kw = {}
    if call_kw is None:
        call_kw = {}
    class _PartialFunction(func):
        def _init(self, *args, **kw):
            args = tuple(init_args) + args
            kw.update(init_kw)
            super(_PartialFunction, self)._init(*args, **kw)

        def _call(self, *args, **kw):
            args = tuple(call_args) + args
            merged_kw = dict(call_kw)
            merged_kw.update(kw)
            return super(_PartialFunction, self)._call(*args, **merged_kw)

        def _parse_params(self, func):
            super(_PartialFunction, self)._parse_params(func)
            self.params = self.params[len(call_args):]
            self.required_params = self.params[len(call_args):]
            self.params = tuple([p for p in self.params if p not in call_kw])
            self.required_params = tuple([p for p in self.required_params if p not in call_kw])
            self.optional_params = tuple([(k, v) for (k, v) in self.optional_params if k not in call_kw])
    return _PartialFunction

def _is_bound_method(func):
    '''
    >>> def foo():
    ...     pass
    >>> _is_bound_method(foo)
    False

    >>> class Foo(object):
    ...     def bar(self):
    ...         pass
    >>> _is_bound_method(Foo.bar)
    False
    >>> _is_bound_method(Foo().bar)
    True
    '''
    return hasattr(func, '__self__') and func.__self__ is not None

if __name__ == '__main__':
    doctest.testmod()
