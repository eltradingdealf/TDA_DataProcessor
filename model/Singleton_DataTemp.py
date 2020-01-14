#!/usr/bin/env python
""" Singleton que contiene las clases
    de modelo con los datos calculados.

    @author Alfredo Sanz
    @date Febrero 2017
"""

#APIs imports

#local imports
from model.Ibex_data import Ibex_data


class Singleton_DataTemp(object):
    class __Singleton_DataTemp:
        def __init__(self):
            self.ibexData = Ibex_data()
        def __str__(self):
            return '-' + str(len(self.ibexData))
    #fin class


    instance = None



    def __new__(cls): # __new__ always a classmethod
        if not Singleton_DataTemp.instance:
            Singleton_DataTemp.instance = Singleton_DataTemp.__Singleton_DataTemp()

        return Singleton_DataTemp.instance
    #fin __new__



    def __getattr__(self, name):
        return getattr(self.instance, name)
    #fin __getattr__



    def __setattr__(self, name):
        return setattr(self.instance, name)
    #fin __setattr__
