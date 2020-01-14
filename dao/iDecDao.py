#!/usr/bin/env python
""" Clase superior que define las funciones 
    para las clases que operan contra la BD
    en los mercados con precios Decimal.

    @author Alfredo Sanz
    @date Marzo 2019
"""

#APIs imports
from abc import ABC, abstractmethod

#local imports


class iDecDAO(ABC):

    @abstractmethod
    def getListTicks_LastByID(self, lastTick_ts):
        pass
    #
#class