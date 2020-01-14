#!/usr/bin/env python
""" Singleton que contiene las clases
    de modelo con los datos calculados
    para mercados con precios en formato decimal..

    @author Alfredo Sanz
    @date Marzo 2019
"""

#APIs imports

#local imports
from model.Dec_data import Dec_data


class Singleton_DataTemp_Dec(object):
    class __Singleton_DataTemp_Dec:
        def __init__(self):
            self.decData = Dec_data()
        def __str__(self):
            return '-' + str(len(self.decData))
    #fin class


    instance = None



    def __new__(cls): # __new__ always a classmethod
        if not Singleton_DataTemp_Dec.instance:
            Singleton_DataTemp_Dec.instance = Singleton_DataTemp_Dec.__Singleton_DataTemp_Dec()

        return Singleton_DataTemp_Dec.instance
    #fin __new__



    def __getattr__(self, name):
        return getattr(self.instance, name)
    #fin __getattr__



    def __setattr__(self, name):
        return setattr(self.instance, name)
    #fin __setattr__