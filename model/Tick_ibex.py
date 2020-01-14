#!/usr/bin/env python
""" Clase contenedora de los datos de un Tick de Ibex 35

    @author Alfredo Sanz
    @date Febrero 2017
"""

#APIs imports

#local imports


class Tick_ibex:

    ID                      = 0
    date                    = 0
    time                    = 0
    mili                    = 0
    ope                     = 0
    trade_price             = 0
    trade_vol               = 0   
    buy_price               = 0
    sell_price              = 0


    def __str__(self):

        result = 'Tick_ibex{'

        result += 'ID=' + str(self.ID)
        result += ', date=' + str(self.date)
        result += ', time=' + str(self.time)
        result += ', mili=' + str(self.mili)
        result += ', ope=' + str(self.ope)
        result += ', trade_price=' + str(self.trade_price)
        result += ', trade_vol=' + str(self.trade_vol)
        result += ', buy_price=' + str(self.buy_price)
        result += ', sell_price=' + str(self.sell_price)
        result += '}'

        return result
    #
#class
