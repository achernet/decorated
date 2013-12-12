# -*- coding: utf-8 -*-
from decorated.base.function import Function, BoundedFunction, PartialFunction
from decorated.decorators.conditional import Conditional
from decorated.decorators.events import Event
from decorated.decorators.once import Once, OnceSession
from decorated.decorators.remove_extra_args import RemoveExtraArgs
from decorated.decorators.retries import Retries

Function = Function
PartialFunction = PartialFunction
BoundedFunction = BoundedFunction

Event = Event
conditional = Conditional
once = Once
OnceSession = OnceSession
remove_extra_args = RemoveExtraArgs
retries = Retries
