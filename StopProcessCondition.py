#!/usr/bin/env python
""" Singleton que contiene Flag de 
    salida del proceso

    @author Alfredo Sanz
    @date Febrero 2017
"""


class StopProcessCondition(type):
    _instances = {}
    stopProcessFlag = False
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(StopProcessCondition, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class StopProcessConditionSingleton(metaclass=StopProcessCondition):
    pass
