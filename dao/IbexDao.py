#!/usr/bin/env python
""" Clase superior que define las funciones 
    para las clases que operan contra MongoDB

    @author Alfredo Sanz
    @date Febrero 2017
"""

#APIs imports
from abc import ABC, abstractmethod

#local imports


class IbexDAO(ABC):

    @abstractmethod
    def getListTicks_LastByID(self, lastTick_ts):
        pass
    #

    @abstractmethod
    def getListTicks_Last1H(self, _curTimeInDate, _time1H_ago):
        pass
    #


    @abstractmethod
    def getListTicks_Last1H_aggregation(self, _curTimeInDate, _time1H_ago):
        pass
    #



    @abstractmethod
    def getListTicks_Last2M(self, _curTimeInDate, _time2M_ago):
        pass
    #
#class