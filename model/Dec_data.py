#!/usr/bin/env python
""" Clase contenedora de los datos calculados
    para futuros con Precios en formato Decimal.

    @author Alfredo Sanz
    @date Marzo 2019
"""

#APIs imports
import logging
import logging.config
from decimal import *
import numpy as np

#local imports
from dataprocess import DataProcessor_util
from common import Constantes


class Dec_data:

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
    current_buy_price       = Decimal("0.0")
    current_sell_price      = Decimal("0.0")

    #ACUMULATED VALUES
    total_vol_sess          = 0
    total_buy_vol_sess      = 0
    total_sell_vol_sess     = 0

    total_volumeprofile_dict    = {} #(key=price<str>, value=vol<int>)  Lista de la sesion completa
    tmp_volumeprofile_dict      = {} #(key=price<str>, value=vol<int>)  Lista parcial del ultimo ciclo.

    #TAPE SPEED
    speedList               = []
    speedTimeToFillList     = 5 #in seconds
    speedT1                 = 0
    speedCurrent            = 0

    #---------------------------------------------
    ticks_array = [[]]
    ticks_array_tmp = []

    volume_ndArray = np.zeros((1, 1), dtype=int) #All the volume Ticks in a 2 dimensions array
    volume_ndArray_tmp = np.zeros(1, dtype=int)
    volumetotal_ndArray = np.zeros(1, dtype=int)  #Store all the volume ticks in a One Dimension array
    deltaStrongFilteredtotal_ndArray = np.zeros(1, dtype=int)  #Stores all the delta strong filtered values
    deltaStrongtotal_ndArray = np.zeros(1, dtype=int)  # Stores all the delta strong values

    arrays_initialized = False
    arrays_index = 0
    #---------------------------------------------

    """
    row 0 -> vol delta
    row 1 -> vol avg
    row 2 -> delta strong
    row 3 -> vol delta Period
    row 4 -> vol Filtered
    row 5 -> Speed
    row 6 -> avg Weight delta Strong filtered
    row 7 -> delta Strong filtered
    row 8 -> avg Weight delta Strong 
    
    One col by candle
    """
    calculatedData_ndArray = np.zeros((9, 1))
    calculatedData_index = 0
    #---------------------------------------------


    def initArrays(self, __market):

        self.logger.info('***Method->initArrays  '+__market+' INIT')

        self.logger.debug('***Method->initArrays  arrays_initialized='+str(self.arrays_initialized))

        if not self.arrays_initialized:
            self.logger.info('***Method->initArrays  arrays NOT initialized')

            self.deltaStrongFilteredtotal_ndArray = np.zeros(1, dtype=int)
            self.deltaStrongtotal_ndArray = np.zeros(1, dtype=int)
            self.volumetotal_ndArray = np.zeros(1, dtype=int)
            self.volume_ndArray = np.zeros((1, Constantes.TICKS_BY_CANDLE[__market]), dtype=int)
            self.volume_ndArray_tmp = np.zeros((1, Constantes.TICKS_BY_CANDLE[__market]), dtype=int)

            self.arrays_initialized = True
            self.arrays_index = 0
            self.logger.info('***Method->initArrays  arrays_index='+str(self.arrays_index)+ ' ENDS')
        #if

        self.logger.debug('***Method->initArrays  ' + __market + ' ENDS')
    #



    def concatenateRowsTmp(self, __market):

        self.logger.debug('***Method->concatenateRowsTmp  INIT')

        self.volume_ndArray = np.concatenate((self.volume_ndArray, self.volume_ndArray_tmp), axis=0)
        self.volume_ndArray_tmp = np.zeros((1, Constantes.TICKS_BY_CANDLE[__market]), dtype=int)
        self.arrays_index = 0

        #New Col for Calculated data array
        tmp = np.zeros((9, 1))
        self.calculatedData_ndArray = np.hstack((self.calculatedData_ndArray, tmp))
        self.calculatedData_index += 1

        self.logger.debug('***Method->concatenateRowsTmp  ENDS')
    #


    def adjustTotalArrays(self, maxElementNumber):

        while True:
            vt_size = np.size(self.volumetotal_ndArray)
            if vt_size > maxElementNumber:
                self.volumetotal_ndArray = np.delete(self.volumetotal_ndArray, 0)
                self.logger.info('***Method->************************************************DELETE A')
            else:
                self.logger.info('***Method->************************************************BREAK A')
                break;
            #if
        #while

        while True:
            dsf_size = np.size(self.deltaStrongFilteredtotal_ndArray)
            if dsf_size > maxElementNumber:
                self.deltaStrongFilteredtotal_ndArray = np.delete(self.deltaStrongFilteredtotal_ndArray, 0)
                self.logger.info('***Method->************************************************DELETE B')
            else:
                self.logger.info('***Method->************************************************BREAK B')
                break;
            #if
        #while

        while True:
            ds_size = np.size(self.deltaStrongtotal_ndArray)
            if ds_size > maxElementNumber:
                self.deltaStrongtotal_ndArray = np.delete(self.deltaStrongtotal_ndArray, 0)
                self.logger.info('***Method->************************************************DELETE C')
            else:
                self.logger.info('***Method->************************************************BREAK C')
                break;
            #if
        #while
    #


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

        self.total_volumeprofile_dict    = {}
        self.tmp_volumeprofile_dict      = {}
    #fin setZeroAcumulatedFields



    def setZeroTmpVolumeProfile(self):
        
       self.tmp_volumeprofile_dict = {}
    #fin setZeroTmpVolumeProfile



    def __str__(self):

        result = 'Dec_data{'

        result += 'current_buy_price=' + str(self.current_buy_price)
        result += ', current_sell_price=' + str(self.current_sell_price)
        result += ', total_vol_sess=' + str(self.total_vol_sess)
        result += ', total_buy_vol_sess=' + str(self.total_buy_vol_sess)
        result += ', total_sell_vol_sess=' + str(self.total_sell_vol_sess)
        result += ', total_volumeprofile_dict=' + repr(self.total_volumeprofile_dict)
        result += ', tmp_volumeprofile_dict=' + repr(self.tmp_volumeprofile_dict)
        result += ', volumetotal_ndArray=' + repr(self.volumetotal_ndArray)

        result += '}'

        return result
    #
#class
