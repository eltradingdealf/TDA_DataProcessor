#!/usr/bin/env python
""" Clase principal para el proceso de ticks de
    los datos de futuros CME con precios en formato decimal

    -REcorre la lista de ticks obtenida de la BD
    -actualiza los datos globales de session
    -Calcula los datos de los periodos.

    @author Alfredo Sanz
    @date Marzo 2019
"""

# APIs imports
import logging
import logging.config
from decimal import Decimal, ROUND_HALF_UP
import numpy as np

# local imports
from dataprocess.DataProcessor import DataProcessor
from model.Singleton_DataTemp_Dec import Singleton_DataTemp_Dec
from common import Constantes
from dataprocess import DataProcessor_util
from common import Util


class DataProcessor_dec(DataProcessor):
    dataSingleton = Singleton_DataTemp_Dec()

    """
    * Constructor
    *
    * Carga el Manejador de Logging
    """

    def __init__(self):

        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('PYDACALC')

    # construct



    """
    * Esta funcion realiza el calculo usando
    * los datos actuales y los nuevos recibidos, actualizando
    * al finalizar el repositorio de datos actuales, disponibles
    * para ser enviados al Host cuando sea necesario.
    """

    def __update_global_data(self, _vol_tmp,
                             _vol_buy_tmp,
                             _vol_sell_tmp,
                             _last_buy_price,
                             _last_sell_price,
                             _profile_vol_tmp):

        errormessage = '0'

        decData = self.dataSingleton.decData

        try:
            # *****PRICE
            if _last_buy_price:
                decData.current_buy_price = _last_buy_price
            #
            if _last_sell_price:
                decData.current_sell_price = _last_sell_price
            #

            # *****VOLUME
            if _vol_tmp:
                decData.total_vol_sess += _vol_tmp
            #
            if _vol_buy_tmp:
                decData.total_buy_vol_sess += _vol_buy_tmp
            #
            if _vol_sell_tmp:
                decData.total_sell_vol_sess += _vol_sell_tmp
            #

            # VOLUME PROFILE TOTAL
            for vpkey in _profile_vol_tmp.keys():
                vp_vol = decData.total_volumeprofile_dict.get(vpkey)

                if vp_vol:
                    vp_vol += _profile_vol_tmp[vpkey]
                else:
                    vp_vol = _profile_vol_tmp[vpkey]
                #

                decData.total_volumeprofile_dict[vpkey] = vp_vol
            # for

            self.logger.debug('decData.total_volumeprofile_dict=' + repr(decData.total_volumeprofile_dict))

            """
            #**VOLUME DELTA**
            self.logger.debug("Calculating delta")
            errormessageD1, d1 = DataProcessor_util.calcDelta(decData.total_buy_vol_sess,
                                                             decData.total_sell_vol_sess,
                                                             self.logger)

            if '0' == errormessageD1:
                decData.acum_delta_sess = d1
            else:
                errormessage = errormessageD1
            #

            #**VOLUME DELTA-F**
            self.logger.debug('Calculating delta-F: decData.acum_delta_sess=' + str(decData.acum_delta_sess) + ',  decData.total_vol_sess=' + str( decData.total_vol_sess))
            errormessageD2, dF  = DataProcessor_util.calcDelta_F(decData.acum_delta_sess, 
                                                              decData.total_vol_sess, 
                                                              self.logger)

            if '0' == errormessageD2:
                decData.acum_deltaF_sess = dF
            else:
                errormessage = errormessageD2
            #
            """

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++Error updating global data in Singleton: ' + repr(ex)

        return errormessage

    # fin __update_global_data



    """
    * Procesa la lista de Ticks de los datos aniadidos a la BBDD
    * desde la ultima consulta.
    * La lista de entrada necesita estar ordenada por que actualizamos
    * el precio actual.
    """

    def __process_tickList_forGlobal(self, _tickList, _errormessage_list):

        self.logger.debug('***Method->__process_tickList_forGlobal tick(for Global): Length tickList=' + str(len(_tickList)) + ' INIT')
        last_ID = '0'

        vol_tmp = 0
        vol_buy_tmp = 0
        vol_sell_tmp = 0
        last_buy_price = 0
        last_sell_price = 0
        profile_vol_tmp = {}

        tckProcessed = 0
        for tick in _tickList:

            try:
                last_ID = tick.ID
                vol_tmp += tick.trade_vol
                self.logger.debug("Process tick(for Global): vol_tmp=" + str(vol_tmp))
                self.logger.debug("Process tick(for Global): tick_ope=" + str(tick.ope))

                # VOLUME
                if Constantes.TICK_OPE_BUY == tick.ope:
                    vol_buy_tmp += tick.trade_vol
                #
                elif Constantes.TICK_OPE_SELL == tick.ope:
                    vol_sell_tmp += tick.trade_vol
                #
                self.logger.debug(
                    "Process tick(for Global): vol_buy_tmp=" + str(vol_buy_tmp) + ", vol_sell_tmp=" + str(vol_sell_tmp))

                # PRICE
                last_buy_price = tick.buy_price
                last_sell_price = tick.sell_price
                self.logger.debug("Process tick(for Global): last_buy_price:" + str(last_buy_price))
                self.logger.debug("Process tick(for Global): last_sell_price:" + str(last_sell_price))

                # VOLUME PROFILE TEMP
                item_volprof = profile_vol_tmp.get(str(tick.trade_price))
                if item_volprof:
                    item_volprof += tick.trade_vol
                    profile_vol_tmp[str(tick.trade_price)] = item_volprof
                else:
                    profile_vol_tmp[str(tick.trade_price)] = tick.trade_vol
                #

            except Exception as ex:
                self.logger.error(repr(ex.args))
                self.logger.exception(ex)
                _errormessage_list.append('++--++do Loop Processing ticks(for Global) Error: ' + repr(ex))
            #

            tckProcessed += 1
        # for

        if 0 < tckProcessed:
            # CON TODOS LOS TICKS SUMADOS -> CALCULAMOS VALORES GLOBALES
            errormessage = self.__update_global_data(vol_tmp,
                                                     vol_buy_tmp,
                                                     vol_sell_tmp,
                                                     last_buy_price,
                                                     last_sell_price,
                                                     profile_vol_tmp)

            if '0' != errormessage:
                _errormessage_list.append(errormessage)
            #
        # if

        self.logger.debug('***Method->__process_tickList_forGlobal tick(for Global) Before update: vol_buy_tmp=' + str(
            vol_buy_tmp) + ', vol_sell_tmp=' + str(vol_sell_tmp) + ' ENDS')
        return _errormessage_list, last_ID, tckProcessed

    # fin __process_tickList_forGlobal



    def calc_speedOfTape(self, decData, tickVol, _currentSpeedT0):
        self.logger.info("***Method->calc_speedOfTape, tickVol: " + str(tickVol) + "  INIT")

        resultSpeed = decData.speedCurrent
        resultSpeedT0 = _currentSpeedT0

        decData.speedList.append(tickVol)

        currTime = Util.getCurrentTimeInSeconds()
        timeDiff = currTime - decData.speedT1
        self.logger.info('??????????????????????????????????? currTime: ' + str(currTime) + ', timeDiff: ' + str(timeDiff))

        if decData.speedTimeToFillList < timeDiff:
            resultSpeed = len(decData.speedList)
            self.logger.info('??????????????????????????????????? resultSpeed: ' + str(resultSpeed))
            decData.speedCurrent = resultSpeed

            decData.speedList = []
            decData.speedT1 = currTime
        #

        if resultSpeed > resultSpeedT0:
            resultSpeedT0 = resultSpeed

        self.logger.info("??????????????????????????????????? Process calc_speedOfTape: resultSpeed=" + str(resultSpeed) + ', resultSpeedT0:' + str(resultSpeedT0))
        self.logger.info("***Method->calc_speedOfTape  ENDS")
        return resultSpeed, resultSpeedT0
    #fin calc_speedOfTape



    def calc_delta(self, decData, period = 0):

        self.logger.debug("***Method->calc_delta  INIT")

        b = 0
        s = 0
        for x in range(decData.arrays_index + 1):
            v = decData.volume_ndArray_tmp[0, x]
            if v >= 0:
                b += v
            else:
                s += v
            #
        #

        #calculate delta for every previous candle according to the period
        b2 = b
        s2 = s
        self.logger.debug('--------------------------------**** period: ' + str(period))
        if 0 < period:
            self.logger.debug('--------------------------------**** range: ' + repr(range(0, period)))

            rowsNumber = np.size(decData.volume_ndArray, 0)
            self.logger.debug('--------------------------------**** rowsNumber: ' + str(rowsNumber))

            for p in range(0, period):
                p += 1
                self.logger.debug('--------------------------------**** p: ' + str(p))
                self.logger.debug('--------------------------------**** decData.volume_ndArray: ' + repr(decData.volume_ndArray))

                if rowsNumber > p:
                    for x in range(np.size(decData.volume_ndArray, 1)):
                        self.logger.debug('--------------------------------**** x: ' + str(x))
                        v2 = decData.volume_ndArray[rowsNumber - p, x]
                        self.logger.debug('--------------------------------**** v2: ' + str(v2))
                        if v2 >= 0:
                            b2 += v2
                        else:
                            s2 += v2
                        #
                    #for
                #if
            #for
        #if


        self.logger.debug("Process __process_tickList: s=" + str(s) + ', b=' + str(b))
        errormessageD1, delta = DataProcessor_util.calcDelta(b, (s * -1), self.logger)
        delta_dec = Decimal(delta)
        delta_dec = Decimal(delta_dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))

        self.logger.debug("Process __process_tickList: s2=" + str(s2) + ', b2=' + str(b2))
        errormessageD1, delta2 = DataProcessor_util.calcDelta(b2, (s2 * -1), self.logger)
        delta_dec2 = Decimal(delta2)
        delta_dec2 = Decimal(delta_dec2.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))

        self.logger.debug("***Method->calc_delta: delta=" + str(delta_dec) + ", delta2: " + str(delta2) + "  ENDS")
        return delta_dec2
    # fin calc_delta



    def calc_delta_byNumberTicks(self, decData, _ndarrNumberTicks):

        self.logger.debug("***Method->calc_delta_byNumberTicks, decData.volumetotal_ndArray: " + repr(decData.volumetotal_ndArray) +"  INIT")

        ndarrSize = np.size(_ndarrNumberTicks)

        #First calculate data for delta of current candle
        b = 0
        s = 0
        for x in range(0, ndarrSize):
            v = _ndarrNumberTicks[x]
            if v >= 0:
                b += v
            else:
                s += v
            #
        #

        self.logger.debug("Process __process_tickList: s=" + str(s) + ', b=' + str(b))
        errormessageD1, delta = DataProcessor_util.calcDelta(b, (s * -1), self.logger)
        delta_dec = Decimal(delta)
        delta_dec = Decimal(delta_dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))

        self.logger.debug("***Method->calc_delta_byNumberTicks: delta_dec: " + str(delta_dec) + "  ENDS")
        return delta_dec
    # fin calc_delta_byNumberTicks



    """
    calculate the total vol of the current candle filtered by the amount of contracts 
    by tick.
    """
    def calc_volFiltered_currentcandle(self, decData):

        self.logger.debug("***Method->calc_volFiltered_currentcandle: volume_ndArray_tmp=" + repr(decData.volume_ndArray_tmp) + ' INIT')

        arTmp = np.absolute(decData.volume_ndArray_tmp[0, :decData.arrays_index + 1])  # quita signo
        arTmp = arTmp[arTmp >= 10]
        vol = np.sum(arTmp)

        self.logger.debug("***Method->calc_volFiltered_currentcandle:  vol=" + str(vol) + ' ENDS')
        return vol
    # fin calc_volFiltered_currentcandle



    def calc_volFiltered_byNumberTicks(self, decData, _ndarrNumberTicks):

        self.logger.debug("***Method->calc_volFiltered_byNumberTicks: volumetotal_ndArray=" + repr(decData.volumetotal_ndArray) + ' INIT')

        result = 0

        arTmp = np.absolute(_ndarrNumberTicks) # quita signo
        arTmp = arTmp[arTmp >= 10]
        result = np.sum(arTmp)

        arTmp2 = _ndarrNumberTicks[_ndarrNumberTicks >= 10]
        arTmp3 = _ndarrNumberTicks[_ndarrNumberTicks <= -10]

        ndarrResult = np.concatenate((arTmp2, arTmp3))
        self.logger.debug("***Method->calc_volFiltered_byNumberTicks: volumetotal_ndArray=" + repr(decData.volumetotal_ndArray) + ' ENDS')

        self.logger.info("***Method->calc_volFiltered_byNumberTicks: ndarrResult=" + repr(ndarrResult) + ' ENDS')
        return result, ndarrResult
    #fin calc_volFiltered_byNumberTicks


    """
    avg vol of ticks
    """
    def calc_avgvol_byNumberTicks(self, decData, _ndarrNumberTicks):

        self.logger.debug("***Method->calc_avgvol_byNumberTicks: _ndarrNumberTicks=" + repr(_ndarrNumberTicks) + ' INIT')

        arTmp = np.absolute(_ndarrNumberTicks)  # quita signo
        self.logger.debug('?????? calc_avgvol_byNumberTicks arTmp: ' + repr(arTmp))
        avg_vol = np.mean(arTmp)                                                       #media
        result = Decimal(avg_vol)
        result = Decimal(result.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))

        self.logger.debug("***Method->calc_avgvol_byNumberTicks:  result=" + str(result) + ' ENDS')
        return result
    # fin calc_avgvol_byNumberTicks



    """
    avg_vol * delta
    """
    def calc_deltaStrong_currentcandle(self, avg_vol_dec, delta_dec):

        self.logger.debug("***Method->calc_deltaStrong_currentcandle: avg_vol_dec=" + repr(avg_vol_dec) + ' INIT')

        strong_dec = Decimal(avg_vol_dec * delta_dec)
        strong_dec = Decimal(strong_dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))

        # copy_sign(other, context=None) -> Return a copy of the first operand with the sign set to be the same
        # as the sign of the second operand.
        # For example: Decimal('2.3').copy_sign(Decimal('-1.5')) --> Decimal('-2.3')
        strong_dec_signal = strong_dec.copy_sign(delta_dec)

        self.logger.debug("***Method->calc_deltaStrong_currentcandle: strong_dec=" + str(strong_dec) + ' ENDS')
        return strong_dec_signal
    # fin calc_deltaStrong_currentcandle


    def calc_deltaStrong_byNumberTicks(self, _vol_filtered, _ndarrFiltered, _numberOfTicks, _speed):

        s, b = DataProcessor_util.calc_sbForDelta_byArr(_ndarrFiltered)
        self.logger.info("????????????????????????????????????????¿???Process calc_deltaStrong_byNumberTicks: s=" + str(s) + ', b=' + str(b))
        errormessageD1, delta = DataProcessor_util.calcDelta(b, (s * -1), self.logger)


        strong = Decimal((((delta * Decimal(0.1)) * _vol_filtered) / _numberOfTicks) * int(_speed))
        result = Decimal(strong.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
        self.logger.info("???????????????????????????????????????????calc_deltaStrong_byNumberTicks: result=" + str(result))

        return result
    #fin calc_deltaString_byNumberTicks



    def getArrayNumberTicks(self, decData, _numberOfTicks=50):

        arSize = np.size(decData.volumetotal_ndArray)
        iStart = 0
        if _numberOfTicks < arSize:
            iStart = arSize - _numberOfTicks - 1
        #

        return decData.volumetotal_ndArray[iStart:]
    #fin getArrayNumberTicks



    """
    * Procesa la lista de Ticks de los datos aniadidos a la BBDD
    * desde la ultima consulta.
    """

    def __process_tickList(self, _tickList, _market, _errormessage_list):

        self.logger.debug('***Method->__process_tickList: Length tickList=' + str(len(_tickList)) + ' INIT')

        tckProcessed = 0
        decData = self.dataSingleton.decData
        decData.initArrays(_market)

        maxColIndex = 0
        maxColNumber = Constantes.TICKS_BY_CANDLE[_market]

        for tick in _tickList:

            try:
                # check if tmp array is full
                self.logger.debug("Process __process_tickList: maxColNumber=" + str(maxColNumber) + 'decData.arrays_index=' + str(decData.arrays_index))
                if maxColNumber <= decData.arrays_index:
                    decData.concatenateRowsTmp(_market)
                #

                # store vol
                self.logger.debug("Process __process_tickList: tick_ope=" + str(tick.ope))
                tickVol = 0
                if Constantes.TICK_OPE_BUY == tick.ope:
                    tickVol = tick.trade_vol
                    decData.volume_ndArray_tmp[0, decData.arrays_index] = tick.trade_vol
                    decData.volumetotal_ndArray = np.append(decData.volumetotal_ndArray, tick.trade_vol)
                #
                elif Constantes.TICK_OPE_SELL == tick.ope:
                    tickVol = -1 * tick.trade_vol
                    decData.volume_ndArray_tmp[0, decData.arrays_index] = -1 * tick.trade_vol
                    decData.volumetotal_ndArray = np.append(decData.volumetotal_ndArray, -1 * tick.trade_vol)
                #
                # positive vol == buy, negative vol == sell
                self.logger.debug("Process __process_tickList: tick vol=" + str(decData.volume_ndArray_tmp[0, decData.arrays_index]))

                ndarrNumberTicks = self.getArrayNumberTicks(decData, maxColNumber)

                # CALC DELTA OF CURRENT CANDLE
                period = 3
                delta_dec = self.calc_delta(decData, period)

                delta_dec2 = self.calc_delta_byNumberTicks(decData, ndarrNumberTicks)

                # CALC AVG VOL FROM THE LAST NUMBER OF TICKS
                avg_vol_dec = self.calc_avgvol_byNumberTicks(decData, ndarrNumberTicks)

                # CALC FILTERED VOLUME
                #vol_filtered = self.calc_volFiltered_currentcandle(decData)
                vol_filtered, ndarrFiltered = self.calc_volFiltered_byNumberTicks(decData, ndarrNumberTicks)

                #SPEED
                speed, speedT0 = self.calc_speedOfTape(decData, tickVol, decData.calculatedData_ndArray[5, decData.calculatedData_index])

                # CALC DELTA STRONG OF CURRENT CANDLE
                # deltaStrong_dec = self.calc_deltaStrong_currentcandle(avg_vol_dec, delta_dec2)
                deltaStrong_dec = self.calc_deltaStrong_byNumberTicks(vol_filtered, ndarrFiltered, maxColNumber, speed)

                #SAVE the data
                decData.calculatedData_ndArray[0, decData.calculatedData_index] = delta_dec
                decData.calculatedData_ndArray[1, decData.calculatedData_index] = avg_vol_dec
                decData.calculatedData_ndArray[2, decData.calculatedData_index] = deltaStrong_dec
                decData.calculatedData_ndArray[3, decData.calculatedData_index] = delta_dec2
                decData.calculatedData_ndArray[4, decData.calculatedData_index] = vol_filtered
                decData.calculatedData_ndArray[5, decData.calculatedData_index] = speedT0

                decData.arrays_index += 1
                self.logger.debug('Process __process_tickList: calculatedData_ndArray:' + repr(decData.calculatedData_ndArray))

            except Exception as ex:
                self.logger.error(repr(ex.args))
                self.logger.exception(ex)
                _errormessage_list.append('++--++do Loop Processing __process_tickList Error: ' + repr(ex))
            #
        # for

        self.logger.debug('***Method->__process_tickList __process_tickList ENDS')
        return _errormessage_list
    # fin __process_tickList



    """
    * Procesa una lista de ticks de datos de Fut_Dec
    *
    * @param _ticklistDict dict{List<Tick_dec>} Dictionary con las Listas de ticks de un futuro CME
    *                           {ticklist_ID | list}
    *
    * @return errormessage_list  lista de Strings con mensajes de error durante el proceso
    *         last_ID   string con el ID del ultimop Tick
    """

    def doProcess(self, _ticklistDict, _thetime, _market):
        """  return errormessage_list [str], last_ID <int> """

        self.logger.debug('***Method->doProcess tick list ' + _market + ' INIT')

        errormessage = '0'
        errormessage_list = []
        last_ID = '0'

        try:
            errormessage_list, last_ID, n1 = self.__process_tickList_forGlobal(_ticklistDict['ticklist_ID'],
                                                                               errormessage_list)

            errormessage_list = self.__process_tickList(_ticklistDict['ticklist_ID'], _market, errormessage_list)

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++do Processing ticks Error: ' + repr(ex)
            errormessage_list.append(errormessage)

        self.logger.debug('***Method->doProcess tick list ' + _market + ' ENDS')
        return errormessage_list, last_ID
    # fin doProcess
# class