#!/usr/bin/env python
""" Clase contenedora de los datos calculados
    para el futuro del Ibex 35

    @author Alfredo Sanz
    @date Febrero 2017
    @update Abril 2017
    @update Marzo 2018
"""

#APIs imports
import logging
import logging.config
import time
import collections
from decimal import *


#local imports
from dataprocess import DataProcessor_util


class Ibex_data():

    """
    * Constructor
    *
    * Carga el Manejador de Logging
    """
    def __init__(self):
        
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('PYDACALC')
    #construct



    #CURRENT VALUES
    current_buy_price       = 0
    current_sell_price      = 0

    #ACUMULATED VALUES
    total_vol_sess          = 0
    total_buy_vol_sess      = 0
    total_sell_vol_sess     = 0
    acum_delta_sess         = 0.0
    acum_deltaF_sess        = 0.0

    #P=2 MINUTES LAST VALUES 
    p2mlast_vol                 = 0
    p2mlast_buy_vol             = 0
    p2mlast_sell_vol            = 0
    p2mlast_delta               = 0.0
    p2mlast_deltaF              = 0.0
    p2mlast_deltaF_avg5m        = 0.0
    p2mlast_deltaF_avg15m       = 0.0

    #P=1 HOUR LAST VALUES
    p1hlast_vol                 = 0
    p1hlast_buy_vol             = 0
    p1hlast_sell_vol            = 0
    p1hlast_delta               = 0.0
    p1hlast_deltaF              = 0.0

    instant_speed_vol_buy       = 0.0
    instant_speed_vol_sell      = 0.0
    instant_speed_vol_delta     = 0.0

    vpoc_price = 0
    vpoc_vol   = 0

    total_volumeprofile_dict    = {} #(key=price<str>, value=vol<int>)  Lista de la sesion completa
    tmp_volumeprofile_dict      = {} #(key=price<str>, value=vol<int>)  Lista parcial del ultimo ciclo.

    #fields not to send
    deltaF2m_periods1M_odict = collections.OrderedDict() #periodos de 1 minuto para delta-f de 2 minutos
    deltaF2m_periods2M_odict = collections.OrderedDict() #periodos de 2 minutos para delta-f de 2 minutos



    def getTotal_volumeprofile_dict_as_lists(self):

        return DataProcessor_util.volumeprofile_dict_to_list(self.total_volumeprofile_dict, self.logger)
    #



    def getTmp_volumeprofile_dict_as_list(self):

        return DataProcessor_util.volumeprofile_dict_to_list(self.tmp_volumeprofile_dict, self.logger)
    #



    def setZeroAcumulatedFields(self):
        
        self.total_vol_sess          = 0
        self.total_buy_vol_sess      = 0
        self.total_sell_vol_sess     = 0
        self.acum_delta_sess         = 0.0

        self.total_volumeprofile_dict    = {}
        self.tmp_volumeprofile_dict      = {}

        self.deltaF2m_periods1M_odict = collections.OrderedDict() #periodos de 1 minuto
        self.deltaF2m_periods2M_odict = collections.OrderedDict() #periodos de 2 minutos
    #fin setZeroAcumulatedFields



    def setZeroTmpVolumeProfile(self):
        
       self.tmp_volumeprofile_dict = {}
    #fin setZeroAcumulatedFields



    def pushDeltaF2m_periods1M(self, position, thevalue):

        thelist = []
        self.logger.info("ibex_data, pushDeltaF2m_periods1M:  position=" + str(position) + ', thevalue=' + str(thevalue))

        if self.deltaF2m_periods1M_odict:
            if position in self.deltaF2m_periods1M_odict:
                thelist = self.deltaF2m_periods1M_odict[position]
            #
        #
        thelist.append(thevalue)
        self.deltaF2m_periods1M_odict[position] = thelist
    #fin pushDeltaF2m_periods1M



    def pushDeltaF2m_periods2M(self, position, thevalue):

        thelist = []
        self.logger.info("ibex_data, pushDeltaF2m_periods2M:  position=" + str(position) + ', thevalue=' + str(thevalue))

        if self.deltaF2m_periods2M_odict:
            if position in self.deltaF2m_periods2M_odict:
                thelist = self.deltaF2m_periods2M_odict[position]
            #
        #
        thelist.append(thevalue)        
        self.deltaF2m_periods2M_odict[position] = thelist
    #fin pushDeltaF2m_periods2M



    """
    * @return [[],[],[]....n]
    """
    def getDeltaF2m_periods1M_lastNpositions(self, npositions_int):
        """
        * Obtiene las listas de las ultimas n posiciones
        """
        result = []

        self.logger.info("ibex_data:  npositions_int=" + str(npositions_int))

        if not self.deltaF2m_periods1M_odict:
            return result;
        #
        
        ks = list(self.deltaF2m_periods1M_odict.keys())
        self.logger.debug("ibex_data:  ks=" + repr(ks) + ', len(ks)=' + str(len(ks)))

        if 0 < len(ks):
            initIndex_int = int(ks[len(ks) -1])
            lastIndex_int = int(ks[len(ks) -1]) + 1 # +1 para la funcion range         
            self.logger.debug("ibex_data:  *initIndex_int=" + str(initIndex_int) + ', lastIndex_int='+ str(lastIndex_int) + ', len(ks)=' + str(len(ks)))

            if len(ks) > npositions_int:
                initIndex_int -= npositions_int
            else:
                initIndex_int -= (len(ks) - 1)
            #
            self.logger.info("ibex_data:  **initIndex_int=" + str(initIndex_int) + ', **lastIndex_int=' + str(lastIndex_int))

            for x in range(initIndex_int, lastIndex_int):
                result.append(self.deltaF2m_periods1M_odict[str(x)])
            #for
        #

        self.logger.debug("ibex_data:  getDeltaF2m_periods1M_lastNpositions result=" + str(len(result)))
        return result
    #fin getDeltaF2m_periods1M_lastNpositions



    """
    * @return [[],[],[]....n]
    """
    def getDeltaF2m_periods2M_lastNpositions(self, npositions_int):
        """
        * Obtiene las listas de las ultimas n posiciones
        """
        result = []

        self.logger.info("ibex_data:  npositions_int=" + str(npositions_int))

        if not self.deltaF2m_periods2M_odict:
            return result;
        #

        ks = list(self.deltaF2m_periods2M_odict.keys())
        self.logger.debug("ibex_data:  ks=" + repr(ks) + ', len(ks)=' + str(len(ks)))

        if 0 < len(ks):
            initIndex_int = int(ks[len(ks) -1])
            lastIndex_int = int(ks[len(ks) -1]) + 1 # +1 para la funcion range         
            self.logger.debug("ibex_data:  *initIndex_int=" + str(initIndex_int) + ', lastIndex_int='+ str(lastIndex_int) + ', len(ks)=' + str(len(ks)))

            if len(ks) > npositions_int:
                initIndex_int -= npositions_int
            else:
                initIndex_int -= (len(ks) - 1)
            #
            self.logger.info("ibex_data:  **initIndex_int=" + str(initIndex_int) + ', **lastIndex_int=' + str(lastIndex_int))

            for x in range(initIndex_int, lastIndex_int):
                result.append(self.deltaF2m_periods2M_odict[str(x)])
            #for
        #

        self.logger.debug("ibex_data:  getDeltaF2m_periods2M_lastNpositions result=" + str(len(result)))
        return result
    #fin getDeltaF2m_periods2M_lastNpositions



    def __str__(self):

        result = 'IbexData{'

        result += 'current_buy_price=' + str(self.current_buy_price)
        result += ', current_sell_price=' + str(self.current_sell_price)
        result += ', total_vol_sess=' + str(self.total_vol_sess)
        result += ', total_buy_vol_sess=' + str(self.total_buy_vol_sess)
        result += ', total_sell_vol_sess=' + str(self.total_sell_vol_sess)
        result += ', acum_delta_sess=' + str(self.acum_delta_sess)
        result += ', p2mlast_vol=' + str(self.p2mlast_vol)
        result += ', p2mlast_buy_vol=' + str(self.p2mlast_buy_vol)
        result += ', p2mlast_sell_vol=' + str(self.p2mlast_sell_vol)
        result += ', p2mlast_delta=' + str(self.p2mlast_delta)
        result += ', p1hlast_vol=' + str(self.p1hlast_vol)
        result += ', p1hlast_buy_vol=' + str(self.p1hlast_buy_vol)
        result += ', p1hlast_sell_vol=' + str(self.p1hlast_sell_vol)
        result += ', p1hlast_delta=' + str(self.p1hlast_delta)
        result += ', instant_speed_vol_buy=' + str(self.instant_speed_vol_buy)
        result += ', instant_speed_vol_sell=' + str(self.instant_speed_vol_sell)
        result += ', instant_speed_vol_delta=' + str(self.instant_speed_vol_delta)
        result += ', total_volumeprofile_dict=' + repr(self.total_volumeprofile_dict)
        result += ', tmp_volumeprofile_dict=' + repr(self.tmp_volumeprofile_dict)
        result += ', vpoc_price=' + str(self.vpoc_price)
        result += ', vpoc_vol=' + str(self.vpoc_vol)
        result += ', deltaF2m_periods1M_odict=' + repr(self.deltaF2m_periods1M_odict)
        result += ', deltaF2m_periods2M_odict=' + repr(self.deltaF2m_periods2M_odict)

        result += '}'

        return result
    #
#class
