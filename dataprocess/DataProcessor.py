#!/usr/bin/env python
""" Clase superior para las clases que van a 
    procesar las listas de ticks.

    @author Alfredo Sanz
    @date Febrero 2017
"""

#APIs imports
from abc import ABC, abstractmethod

#local imports


class DataProcessor(ABC):

    """
    * Procesa una lista de ticks
    """
    @abstractmethod
    def doProcess(self, tickList):
        pass
    #
#class
