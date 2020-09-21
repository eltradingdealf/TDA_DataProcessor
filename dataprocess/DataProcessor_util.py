#!/usr/bin/env python
""" Common File
    Utility functions data calculation process
    
    @author Alfredo Sanz
    @date Agosto 2017
"""
#APIs imports
from decimal import Decimal, ROUND_HALF_UP
import numpy as np

#local Imports
from common import Constantes


"""
* Delta-F es el calculo de la fuerza que tiene un valor Delta de volumen.
* El delta es un porcentaje, calculado a partir de la diff entre vol de venta y compra.
* Aquí ponderamos ese porcentaje con el volumen total del periodo, de forma que obtengamos
* un valor mas alto cuanto mas volumen haya.
*
* @param _delta Valor Real con el porcentaje delta de volumen del periodo.
* @param _volTotal Valor Entero con el dato de volumen total del periodo.
*
* @return  Valor Real con el dato de Delta-F
"""
def calcDelta_F(_delta, _volTotal, _logger):

    errormessage = '0'
    result_dec = Decimal(0.0)

    try:
        val = (_delta * _volTotal) / 100
        dec = Decimal(val)
        result_dec = Decimal(dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
        _logger.debug('calcDelta-F: ' + str(result_dec))

    except Exception as ex:
        _logger.error(repr(ex.args))
        _logger.exception(ex)
        errormessage = '++--++Error Calculating Delta-F value: ' + repr(ex)

    return errormessage, result_dec
#fin calDelta_F




"""
* position = ((HH-8) * 60 + MM)
*
* @return str
"""
def calculatePositionArrayByTime_1M(_hour, _minute):
    """
    *Funcion para calcular la posicion en un array que almacena datos
    *en periodos de 1 minutos.
    """

    result = 0

    HH = _hour - 8  #8 is trading hour init
    result = int(HH * 60 + _minute)

    return str(result)
#fin calculatePositionArrayByTime_1M



"""
* position = ((HH * 60 + MM) - (MM Mod 2)) / 2
*
* @return str
"""
def calculatePositionArrayByTime_2M(_hour, _minute):
    """
    *Funcion para calcular la posicion en un array que almacena datos
    *en periodos de 2 minutos.
    """

    result = 0

    HH = _hour - 8  #8 is trading hour init
    mod2 = _minute % 2
    result = int(((HH * 60 + _minute) - mod2) / 2)

    return str(result)
#fin calculatePositionArrayByTime_2M



def calc_sbForDelta_byArr(_theArr):

    result_S = 0
    result_B = 0
    arTmpSize = np.size(_theArr)

    for x in range(0, arTmpSize):
        v = _theArr[x]
        if v >= 0:
            result_B += v
        else:
            result_S += v
        #
    #

    return result_S, result_B
#fin calc_sbForDelta_byArr


"""
* Delta es un valor en tanto por ciento que representa la
* diferencia entre volumen de compra y de venta..
* Es un valor Real.
* Vamos a utilizar un solo Decimal.
*
* @param _buy Valor entero con la cantidad de vol de compra
* @param _sell Valor entero con la cantidad de vol de venta
*
* @return Valor Real con un solo decimal.
"""
def calcDelta(_buy, _sell, _logger):
    """ return errormessage, result_dec <Decimal> """

    errormessage = '0'
    result_dec = Decimal(0.0)

    try:
        if _buy != _sell:

            if _buy > _sell:
                val = ((_buy - _sell) * 100) / _buy
                dec = Decimal(val)
                result_dec = Decimal(dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
                _logger.debug('calcDelta A %: ' + str(result_dec))
            #
            else:
                val = (((_sell - _buy) * 100) / _sell) * -1
                dec = Decimal(val)
                result_dec = Decimal(dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
                _logger.debug('calcDelta B %: ' + str(result_dec))
            #
        #
    except Exception as ex:
        _logger.error(repr(ex.args))
        _logger.exception(ex)
        errormessage = '++--++Error Calculating Delta values: ' + repr(ex)

    return errormessage, result_dec
#fin __calcDelta



def calcDelta_decimal(_buy_dec, _sell_dec, _logger):
    """ return errormessage, result_dec <Decimal> """

    errormessage = '0'
    result_dec = Decimal(0.0)

    try:
        if _buy_dec != _sell_dec:

            if _buy_dec > _sell_dec:
                val_dec = ((_buy_dec - _sell_dec) * 100) / _buy_dec
                result_dec = Decimal(val_dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
                _logger.debug('calcDelta A %: ' + str(result_dec))
            #
            else:
                val_dec = (((_sell_dec - _buy_dec) * 100) / _sell_dec) * -1
                result_dec = Decimal(val_dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
                _logger.debug('calcDelta B %: ' + str(result_dec))
            #
        #
    except Exception as ex:
        _logger.error(repr(ex.args))
        _logger.exception(ex)
        errormessage = '++--++Error Calculating Delta_decimal values: ' + repr(ex)

    return errormessage, result_dec
#fin calcDelta_decimal



def minusOneSecondFromCurrent(ihour, iminute, isecond):

    if isecond > 0:
        isecond -= 1
    else:
        isecond = 59

        if iminute > 0:
            iminute -= 1
        else:
            iminute = 59

            if ihour > 0:
                ihour -= 1
            else:
                ihour = 23
            #
        #
    #
    
    return ihour, iminute, isecond
#fin minusOneSecondFromCurrent



def checkTicktimeGreaterCurrentRange(tick_time, tick_mili, ihour, iminute, isecond, imilisec):

    #tick time splited
    time_str = str(tick_time)

    if 5 == len(time_str):
        time_str = '0' + time_str
    #

    tick_ihour = int(time_str[:2])
    tick_iminute = int(time_str[2:4])
    tick_isecond = int(time_str[4:])

    if tick_ihour > ihour:
        return True
    elif tick_ihour == ihour:
        if tick_iminute > iminute:
            return True
        elif tick_iminute == iminute:
            if tick_isecond > isecond:
                return True
            elif tick_isecond == isecond:
                if tick_mili >= imilisec:
                    return True
                #
            #
        #
    #

    return False #si no se encontro ningun caso True
#fin checkTicktimeGreaterCurrentRange




"""
* Transforma el diccionario con los precios y su volumen a una dos strings
* que contiene cada uno de ellos una lista separada por comas.
"""
def volumeprofile_dict_to_list(_volumeprofile_dict, _logger):
    """ return result_prices<str>,  result_volumes<str> """
    
    result_prices = ''
    result_volumes = ''

    if(0 == len(_volumeprofile_dict)):
        result_prices = '0'
        result_volumes = '0'

        _logger.info('result_prices=' + result_prices + ', result_volumes=' + result_volumes)
        return result_prices, result_volumes
    #

    vpkeys_list = list(_volumeprofile_dict.keys())  #las keys del dict son str
    vpkeys_list = [int(_key) for _key in vpkeys_list] #las pasamos todas a int para poder ordenar bien. list comphrension, @see https://docs.python.org/3/howto/functional.html
    vpkeys_list.sort(reverse=True)

    first = True
    for vpkey in vpkeys_list:
        if first:
            first = False
        else:
            result_prices += ','
            result_volumes += ','
        #

        result_prices += str(vpkey)
        result_volumes += str(_volumeprofile_dict[str(vpkey)])
    #

    _logger.info('result_prices=' + result_prices + ', result_volumes=' + result_volumes)
    return result_prices, result_volumes
#fin volumeprofile_dict_to_list