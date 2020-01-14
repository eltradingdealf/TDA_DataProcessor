#!/usr/bin/env python
""" Clase principal para el proceso de ticks de
    los datos del Ibex35

    -REcorre la lista de ticks obtenida de la BD
    -actualiza los datos globales de session
    -Calcula los datos de los periodos.

    @author Alfredo Sanz
    @date Febrero 2017
"""

#APIs imports
import logging
import logging.config
import time
from decimal import Decimal, ROUND_HALF_UP

#local imports
from dataprocess.DataProcessor import DataProcessor
from model.Ibex_data import Ibex_data
from model.Singleton_DataTemp import Singleton_DataTemp
from model.Tick import Tick
from common import Constantes
from dataprocess import DataProcessor_util




class DataProcessor_ibex(DataProcessor):

    dataSingleton = Singleton_DataTemp()

    """
    * Constructor
    *
    * Carga el Manejador de Logging
    """
    def __init__(self):

        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('PYDACALC')
    #construct



    """
    * Esta funcion Realiza la funcion de calculo usando
    * los datos actuales y los nuevos recibidos, actualizando
    * al finalizar el repositorio de datos actuales, disponibles
    * para ser enviados al Host cuando sea necesario.
    """
    def __updateData_LastID(self, _vol_tmp, 
                                  _vol_buy_tmp, 
                                  _vol_sell_tmp, 
                                  _last_buy_price,
                                  _last_sell_price,
                                  _profile_vol_tmp):

        errormessage = '0'

        ibxData = self.dataSingleton.ibexData

        try:
            #*****PRICE
            if _last_buy_price:
                ibxData.current_buy_price = _last_buy_price
            #
            if _last_sell_price:
                ibxData.current_sell_price = _last_sell_price
            #

            #*****VOLUME
            if _vol_tmp:
                ibxData.total_vol_sess += _vol_tmp
            #
            if _vol_buy_tmp:
                ibxData.total_buy_vol_sess += _vol_buy_tmp
            #
            if _vol_sell_tmp:
                ibxData.total_sell_vol_sess += _vol_sell_tmp
            #

            #VOLUME PROFILE TOTAL
            for vpkey in _profile_vol_tmp.keys(): 
                vp_vol = ibxData.total_volumeprofile_dict.get(vpkey)

                if vp_vol:
                    vp_vol += _profile_vol_tmp[vpkey]
                else:
                    vp_vol = _profile_vol_tmp[vpkey]
                #

                ibxData.total_volumeprofile_dict[vpkey] = vp_vol
            #for

            #VOLUME PROFILE TMP
            for vpkey in _profile_vol_tmp.keys(): 
                vp_vol = ibxData.tmp_volumeprofile_dict.get(vpkey)

                if vp_vol:
                    vp_vol += _profile_vol_tmp[vpkey]
                else:
                    vp_vol = _profile_vol_tmp[vpkey]
                #

                ibxData.tmp_volumeprofile_dict[vpkey] = vp_vol
            #for

            self.logger.debug('ibxData.tmp_volumeprofile_dict=' + repr(ibxData.tmp_volumeprofile_dict))
            self.logger.debug('ibxData.total_volumeprofile_dict=' + repr(ibxData.total_volumeprofile_dict))

            #VPOC
            vpoc_price = 0
            vpoc_vol = 0
            for vpkey in ibxData.total_volumeprofile_dict.keys():
                vp_vol = ibxData.total_volumeprofile_dict[vpkey]
                
                if vp_vol > vpoc_vol:
                    vpoc_vol = vp_vol
                    vpoc_price = int(vpkey)
                #
                self.logger.debug('*** VPOC=???????????? vpkey=' + str(vpkey) + ', vp_vol=' + str(vp_vol) + ', vpoc_vol:' + str(vpoc_vol) + ', + vpoc_price=' + str(vpoc_price))
            #for
            ibxData.vpoc_vol = vpoc_vol
            ibxData.vpoc_price = vpoc_price

            #**VOLUME DELTA**
            self.logger.debug("Calculating delta")
            errormessageD1, d1 = DataProcessor_util.calcDelta(ibxData.total_buy_vol_sess,
                                                              ibxData.total_sell_vol_sess,
                                                              self.logger)

            if '0' == errormessageD1:
                ibxData.acum_delta_sess = d1
            else:
                errormessage = errormessageD1
            #

            #**VOLUME DELTA-F**
            self.logger.debug('Calculating delta-F: ibxData.acum_delta_sess=' + str(ibxData.acum_delta_sess) + ',  ibxData.total_vol_sess=' + str( ibxData.total_vol_sess))
            errormessageD2, dF  = DataProcessor_util.calcDelta_F(ibxData.acum_delta_sess, 
                                                               ibxData.total_vol_sess, 
                                                               self.logger)

            if '0' == errormessageD2:
                ibxData.acum_deltaF_sess = dF
            else:
                errormessage = errormessageD2
            #

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++Error updating global data in Singleton: ' + repr(ex)

        return errormessage
    #fin __updateData_LastID




    """
    * Estos datos siempre son valores totales, no se
    * acumulan a los datos anteriores, ya que hemos calculado
    * todos los ticks del periodo.
    """
    def __updateData_Last1H(self, _vol_tmp, 
                                  _vol_buy_tmp, 
                                  _vol_sell_tmp):

        errormessage = '0'

        ibxData = self.dataSingleton.ibexData

        try:
            #*****VOLUME
            if _vol_tmp:
                ibxData.p1hlast_vol = _vol_tmp
            #
            if _vol_buy_tmp:
                ibxData.p1hlast_buy_vol = _vol_buy_tmp
            #
            if _vol_sell_tmp:
                ibxData.p1hlast_sell_vol = _vol_sell_tmp
            #

            #**VOLUME DELTA**
            self.logger.debug("Calculating delta: ibxData.p1hlast_buy_vol=" + str(ibxData.p1hlast_buy_vol) + ",  ibxData.p1hlast_sell_vol=" + str( ibxData.p1hlast_sell_vol))
            errormessageD1, d1  = DataProcessor_util.calcDelta(ibxData.p1hlast_buy_vol, 
                                                               ibxData.p1hlast_sell_vol, 
                                                               self.logger)
            if '0' == errormessageD1:
                ibxData.p1hlast_delta = d1
            else:
                errormessage = errormessageD1
            #

            #**VOLUME DELTA-F**
            self.logger.debug('Calculating delta-F: ibxData.p1hlast_buy_vol=' + str(ibxData.p1hlast_vol) + ',  ibxData.p1hlast_delta=' + str( ibxData.p1hlast_delta))
            errormessageD2, dF  = DataProcessor_util.calcDelta_F(ibxData.p1hlast_delta, 
                                                               ibxData.p1hlast_vol, 
                                                               self.logger)
            if '0' == errormessageD2:
                ibxData.p1hlast_deltaF = dF
            else:
                errormessage = errormessageD2
            #

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++Error updating LAST-1H data in Singleton: ' + repr(ex)

        return errormessage
    #fin __updateData_Last1H




    """
    * Estos datos siempre son valores totales, no se
    * acumulan a los datos anteriores, ya que hemos calculado
    * todos los ticks del periodo.
    """
    def __updateData_Last2M(self, _vol_tmp, 
                                  _vol_buy_tmp, 
                                  _vol_sell_tmp,
                                  _position1M_str, 
                                  _position2M_str):

        errormessage = '0'

        ibxData = self.dataSingleton.ibexData

        try:
            #*****VOLUME
            ibxData.p2mlast_vol = 0
            ibxData.p2mlast_buy_vol = 0
            ibxData.p2mlast_sell_vol = 0
            
            if _vol_tmp:
                ibxData.p2mlast_vol = _vol_tmp
            #
            if _vol_buy_tmp:
                ibxData.p2mlast_buy_vol = _vol_buy_tmp
            #
            if _vol_sell_tmp:
                ibxData.p2mlast_sell_vol = _vol_sell_tmp
            #

            #**VOLUME DELTA**
            self.logger.debug('Calculating delta: ibxData.p2mlast_buy_vol=' + str(ibxData.p2mlast_buy_vol) + ',  ibxData.p2mlast_sell_vol=' + str( ibxData.p2mlast_sell_vol))
            errormessageD1, d1  = DataProcessor_util.calcDelta(ibxData.p2mlast_buy_vol, 
                                                               ibxData.p2mlast_sell_vol, 
                                                               self.logger)
            if '0' == errormessageD1:
                ibxData.p2mlast_delta = d1
            else:
                errormessage = errormessageD1
            #

            #**VOLUME DELTA-F**
            self.logger.debug('Calculating delta-F: ibxData.p2mlast_vol=' + str(ibxData.p2mlast_vol) + ',  ibxData.p2mlast_delta=' + str( ibxData.p2mlast_delta))
            errormessageD2, dF  = DataProcessor_util.calcDelta_F(ibxData.p2mlast_delta, 
                                                               ibxData.p2mlast_vol, 
                                                               self.logger)
            if '0' == errormessageD2:
                ibxData.p2mlast_deltaF = dF
                ibxData.pushDeltaF2m_periods1M(_position1M_str, dF)
                ibxData.pushDeltaF2m_periods2M(_position2M_str, dF)
            else:
                errormessage = errormessageD2
            #

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++Error updating LAST-2M data in Singleton: ' + repr(ex)

        return errormessage
    #fin __updateData_Last2M



    """
    * Estos datos siempre son valores totales, no se
    * acumulan a los datos anteriores, ya que hemos calculado
    * todos los ticks del periodo.
    """
    def __updateData_instantSpeed_vol(self, _instant_speed_buy, 
                                            _instant_speed_sell,
                                            _instant_speed_delta):

        errormessage = '0'

        ibxData = self.dataSingleton.ibexData

        try:
            ibxData.instant_speed_vol_buy = _instant_speed_buy
            ibxData.instant_speed_vol_sell = _instant_speed_sell
            ibxData.instant_speed_vol_delta = _instant_speed_delta

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++Error updating Instant Speed data data in Singleton: ' + repr(ex)

        return errormessage
    #fin __updateData_instantSpeed_vol



    """
    * Procesa la lista de Ticks de los datos aniadidos a la BBDD
    * desde la ultima consulta.
    * La lista de entrada necesita estar ordenada por que actualizamos
    * el precio actual.
    """
    def __processLastID_tickList(self, _tickList, _errormessage_list):

        self.logger.debug('***Method->__processLastID_tickList tick(LAST-ID): Length tickList='+ str(len(_tickList)))
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
                self.logger.info("Process tick(LAST-ID): vol_tmp="+ str(vol_tmp))

                #VOLUME
                if Constantes.TICK_OPE_BUY == tick.ope:
                    vol_buy_tmp += tick.trade_vol
                #
                elif Constantes.TICK_OPE_SELL == tick.ope:
                    vol_sell_tmp += tick.trade_vol
                #
                self.logger.debug("Process tick(LAST-ID): vol_buy_tmp="+ str(vol_buy_tmp) + ", vol_sell_tmp=" + str(vol_sell_tmp))

                #PRICE
                last_buy_price = tick.buy_price
                last_sell_price = tick.sell_price                          

                #VOLUME PROFILE TEMP
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
                _errormessage_list.append('++--++do Loop Processing ticks(LAST-ID) Error: ' + repr(ex))
            #

            tckProcessed += 1
        #for

        if 0 < tckProcessed:
            #CON TODOS LOS TICKS SUMADOS -> CALCULAMOS VALORES GLOBALES
            errormessage = self.__updateData_LastID(vol_tmp, 
                                                    vol_buy_tmp, 
                                                    vol_sell_tmp, 
                                                    last_buy_price,
                                                    last_sell_price,
                                                    profile_vol_tmp)

            if '0' != errormessage:
                _errormessage_list.append(errormessage)
            #
        #if

        self.logger.debug('***Method->__processLastID_tickList tick(LAST-ID) Before update: vol_buy_tmp='+ str(vol_buy_tmp) + ', vol_sell_tmp=' + str(vol_sell_tmp))
        return _errormessage_list, last_ID, tckProcessed
    #fin __processLastID_tickList



    """
    * Procesa la lista de Ticks de la ultima hora.
    * Esta lista no necesita ordenacion porque solo se suman los valores.
    """
    def __processLast1H_tickList(self, _tickList, _errormessage_list):
        
        self.logger.debug('***Method->__processLast1H_tickList tick(LAST-1H): Length tickList='+ str(len(_tickList)))
        
        vol_tmp = 0
        vol_buy_tmp = 0
        vol_sell_tmp = 0

        i = 0
        for tick in _tickList:
            
            try:
                vol_tmp += tick.trade_vol

                #VOLUME
                if Constantes.TICK_OPE_BUY == tick.ope:
                    vol_buy_tmp += tick.trade_vol
                
                elif Constantes.TICK_OPE_SELL == tick.ope:
                    vol_sell_tmp += tick.trade_vol
                #
                self.logger.debug("Process tick(LAST-1H): vol_buy_tmp="+ str(vol_buy_tmp) + ", vol_sell_tmp=" + str(vol_sell_tmp))

            except Exception as ex:
                self.logger.error(repr(ex.args))
                self.logger.exception(ex)
                _errormessage_list.append('++--++do Loop Processing ticks(LAST-1H) Error: ' + repr(ex))
            #

            i += 1
        #for

        #CON TODOS LOS TICKS SUMADOS -> CALCULAMOS VALORES GLOBALES
        errormessage = self.__updateData_Last1H(vol_tmp, 
                                                vol_buy_tmp, 
                                                vol_sell_tmp)

        if '0' != errormessage:
            _errormessage_list.append(errormessage)
        #

        self.logger.debug('***Method->__processLast1H_tickList Ticks(LAST-1H) processed: ' + str(i) + ', errormessages num: ' + str(len(_errormessage_list)))
        return _errormessage_list, i
    #fin __processLast1H_tickList



    """
    * Procesa la lista de Ticks de los ultimos dos minutos.
    * Esta lista no necesita ordenacion porque solo se suman los valores.
    """
    def __processLast2M_tickList(self, _tickList, position1M_str, position2M_str, _errormessage_list):
        
        self.logger.debug('***Method->__processLast2M_tickList (LAST-2M): Length tickList=' + str(len(_tickList)))
        
        vol_tmp = 0
        vol_buy_tmp = 0
        vol_sell_tmp = 0

        i = 0
        for tick in _tickList:
            
            try:
                vol_tmp += tick.trade_vol

                #VOLUME
                if Constantes.TICK_OPE_BUY == tick.ope:
                    vol_buy_tmp += tick.trade_vol
                
                elif Constantes.TICK_OPE_SELL == tick.ope:
                    vol_sell_tmp += tick.trade_vol
                #
                self.logger.debug("Process tick(LAST-2M): vol_buy_tmp="+ str(vol_buy_tmp) + ", vol_sell_tmp=" + str(vol_sell_tmp))

            except Exception as ex:
                self.logger.error(repr(ex.args))
                self.logger.exception(ex)
                _errormessage_list.append('++--++do Loop Processing ticks(LAST-2M) Error: ' + repr(ex))
            #

            i += 1
        #for

        
        #CON TODOS LOS TICKS SUMADOS -> CALCULAMOS VALORES GLOBALES
        errormessage = self.__updateData_Last2M(vol_tmp, 
                                                vol_buy_tmp, 
                                                vol_sell_tmp,
                                                position1M_str, 
                                                position2M_str)

        if '0' != errormessage:
            _errormessage_list.append(errormessage)
        #

        self.logger.debug('***Method->__processLast2M_tickList (LAST-2M) processed: ' + str(i) + ', errormessages num: ' + str(len(_errormessage_list)))
        return _errormessage_list, i
    #fin __processLast2M_tickList



    """
    * Divide los datos de volumen de los ultimos quince segundos en un array de
    * 15 posiciones, cada posicion la sumatoria de los datos de volumen de un segundo.
    *
    * Devuelve un array de 15 posiciones, la primera posicion es el segundo mas reciente.
    """
    def __splitTicksByOneSecondPeriods(self, _thetime, _tickList):
        """ return  periods_buy_list [int], periods_sell_list[int]"""

        self.logger.debug('Process Instant Speed Period data split INIT')

        periods_buy_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  #len == 15
        periods_sell_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #len == 15

        try:
            #El Rango del pimer periodo va desde la hora actual a hora actual - 1 segundo.
            #Restamos 1 segundo a la Hora,minuto,segundo actual, para establecer el primer periodo L1
            self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  current.hour='+str(_thetime['hour']) + ', current.minute=' + str(_thetime['minute'])+ ', current.second=' + str( _thetime['second']))
            ihour, iminute, isecond = DataProcessor_util.minusOneSecondFromCurrent( _thetime['hour'], _thetime['minute'], _thetime['second'])
            imilisec = _thetime['milisec']
            cur_period = 0

            #recorremos la lista de 1H al reves, empezando por el ultimo
            for tick in reversed(_tickList):
                
                #Comprobamos que la hora tick sea mayor que el limite periodo
                #Si la hora es inferior, cambiamos periodo
                self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  tick.time='+str(tick.time) + ', tick.mili=' + str(tick.mili))
                self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  ihour='+str(ihour) + ', iminute='+str(iminute) + ', isecond='+str(isecond) + ', imilisec='+str(imilisec))
                while not DataProcessor_util.checkTicktimeGreaterCurrentRange(tick.time, tick.mili, ihour, iminute, isecond, imilisec):
                    self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  TICK out range')
                    ihour, iminute, isecond = DataProcessor_util.minusOneSecondFromCurrent(ihour, iminute, isecond)
                    self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$-2  ihour='+str(ihour) + ', iminute='+str(iminute) + ', isecond='+str(isecond) + ', imilisec='+str(imilisec))
                    cur_period += 1

                    if 15 == cur_period:
                        self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  breaking WHILE loop, cur_period='+str(cur_period) + ',')
                        break
                    #
                #
                self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  cur_period='+str(cur_period) + ',')
                if 15 == cur_period:
                    self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  breaking FOR loop, cur_period='+str(cur_period) + ',')
                    break
                #

                if Constantes.TICK_OPE_BUY == tick.ope:
                    periods_buy_list[cur_period] += tick.trade_vol
                    self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  periods_buy_list='+repr(periods_buy_list))
                
                elif Constantes.TICK_OPE_SELL == tick.ope:
                    periods_sell_list[cur_period] += tick.trade_vol
                    self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$  periods_sell_list='+repr(periods_sell_list))
                #
            #for
            

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            _errormessage_list.append('++--++do Loop Processing calc of vol by periods(LAST-1H list) Error: ' + repr(ex))
        #

        self.logger.debug('Process Instant Speed Period data split ENDS')
        return periods_buy_list, periods_sell_list
    #fin __splitTicksByOneSecondPeriods



    """
    * La velocidad Instantanea la calculamos con una media exponencial.
    * Para ello, aplicamos un peso a cada sumatoria de valores del periodo.
    * Al periodo mas reciente, el de la posicion 0, le aplicamos el peso mas alto.
    * La media se calcula dividiendo la sumatoria del resultado de multiplicar cada
    *     valor por su pesos entre la sumatoria de los pesos.
    """
    def __calculate_InstantSpeed(self, periods_list):
        """ return result_exp_average <Decimal value, 1 decimal position> """

        result_exp_average = 0

        weight_total = 0
        weighted_value_total = 0
        i = 15
        #recorremos al reves, porque queremos dar el mayor
        #peso a la primera posicion.
        for value in periods_list:
            self.logger.debug('######### INSTANT SPEED;  value=' + str(value))
            #peso
            weight = i * i
            weight_total += weight

            weighted_value = value * weight             
            weighted_value_total += weighted_value
            self.logger.debug('######### INSTANT SPEED;  i=' + str(i))
            self.logger.debug('######### INSTANT SPEED;  weight=' + str(weight))
            self.logger.debug('######### INSTANT SPEED;  weight_total=' + str(weight_total))
            self.logger.debug('######### INSTANT SPEED;  weighted_value=' + str(weighted_value))
            self.logger.debug('######### INSTANT SPEED;  weighted_value_total=' + str(weighted_value_total))
            i -= 1
        #for

        exp_average = weighted_value_total / weight_total
        exp_average_dec = Decimal(exp_average)
        result_exp_average = Decimal(exp_average_dec.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
        
        self.logger.debug('######### INSTANT SPEED;  exp_average=' + str(result_exp_average))
        return result_exp_average
    #fin __calculate_InstantSpeed



    """
    * Realiza el calculo de la Velocidad instantanea del volumen.
    * Los datos los obtenemos de la lista 1H, ya que queremos los ultimos 15 segundos.
    *
    * El calculo consiste en una media exponencial de 15 periodos. Cada periodo es 1 segundo.
    * Obtenemos los datos de cada segundo leyendo la lista de 1H.
    *
    * Para cada segundo se suman los volumenes y se multiplican por un peso.
    * El Primer segundo, el mas reciente, tendra el peso mas alto.
    *
    * Una vez calculada la media exp de los volumenes de compra y venta, se calcula el delta.
    *  
    """
    def _process_InstantSpeed_vol(self, _tickList, _thetime, _errormessage_list):

        self.logger.debug('***Method->_process_InstantSpeed_vol, ticklist=LAST-1H INIT')
        
        try:
            periods_buy_list, periods_sell_list = self.__splitTicksByOneSecondPeriods(_thetime, _tickList)
            self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$ buy_list=' + repr(periods_buy_list))
            self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$ sell_list='+ repr(periods_sell_list))

            #CALCULATE EXP AVERAGE
            instant_speed_buy  = self.__calculate_InstantSpeed(periods_buy_list)
            instant_speed_sell = self.__calculate_InstantSpeed(periods_sell_list)
            self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$ instant_speed_buy=' + str(instant_speed_buy) +', instant_speed_sell=' + str(instant_speed_sell))

            #CALCULATE DELTA EXP AVERAGE
            errormessage, instant_speed_delta = DataProcessor_util.calcDelta_decimal(instant_speed_buy, instant_speed_sell, self.logger)
            self.logger.debug('$$$$$$$$$$$$$$$$$$$$$$ Delta=' + str(instant_speed_delta))


            #SAVE DATA
            errormessage = self.__updateData_instantSpeed_vol(instant_speed_buy, instant_speed_sell, instant_speed_delta)

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            _errormessage_list.append('++--++do Calculate Instant Speed with volume Error: ' + repr(ex))
        #

        if '0' != errormessage:
            _errormessage_list.append(errormessage)
        #

        self.logger.debug('***Method->_process_InstantSpeed_vol, ticklist=LAST-1H ENDS')
        return _errormessage_list
    #fin _process_InstantSpeed_vol



    def _calculateAverages(self, position1M_str, position2M_str, _errormessage_list):
        """
        * Calculate averages.
        *    -Avg for DeltaF values. Delta-F's values calculated from last 2minutes and stored
        *               in 1minute array period, we take 5 and 15 minutes periods, and average it.
        """
        self.logger.info('***Method->_calculateAverages INIT')
        
        ibxData = self.dataSingleton.ibexData

        try:
            #AVG FOR DELTA-F 2M, PERIOD 5 MINS            
            deltaF2m_1Mper_nposit_list = ibxData.getDeltaF2m_periods1M_lastNpositions(5)
            totalValue_int = 0
            totalItems = 0
            for period_list in deltaF2m_1Mper_nposit_list:
                for value_int in period_list:
                    totalValue_int += value_int
                    totalItems += 1
                #for
            #for

            val5 = totalValue_int / totalItems
            dec5 = Decimal(val5)
            av5m_dec = Decimal(dec5.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))

            #AVG FOR DELTA-F 2M, PERIOD 15 MINS            
            deltaF2m_1Mper_nposit_15_list = ibxData.getDeltaF2m_periods1M_lastNpositions(15)
            totalValue15_int = 0
            totalItems15 = 0
            for period_15_list in deltaF2m_1Mper_nposit_15_list:
                for value_15_int in period_15_list:
                    totalValue15_int += value_15_int
                    totalItems15 += 1
                #for
            #for

            val15 = totalValue15_int / totalItems15
            dec15 = Decimal(val15)
            av15m_dec = Decimal(dec15.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))

            ibxData.p2mlast_deltaF_avg5m = av5m_dec
            ibxData.p2mlast_deltaF_avg15m = av15m_dec
            self.logger.info("av5m_dec=" + str(av5m_dec) + ', av15m_dec=' + str(av15m_dec))

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            _errormessage_list.append('++--++do Calculate averages Error: ' + repr(ex))
        #

        self.logger.info('***Method->_calculateAverages ENDS')
        return _errormessage_list
    #fin _calculateAverages



    """
    * Procesa una lista de ticks de datos de Fut_ibex35
    *
    * @param _ticklistDict dict{List<Tick_ibex>} Dictionary con las Listas de ticks del Ibex
    *                           {ticklist_ID, ticklist_P1H, ticklist_P2M | list}
    *
    * @return errormessage_list  lista de Strings con mensajes de error durante el proceso
    *         last_ID   string con el ID del ultimop Tick
    """
    def doProcess(self, _ticklistDict, _thetime):
        """  return errormessage_list [str], last_ID <int> """
        
        self.logger.info('***Method->doProcess tick list INIT')

        errormessage = '0'
        errormessage_list = []
        last_ID = '0'

        try:
            #posicion de array para el momento actual, para guardar informacion por periodos
            position1M_str = DataProcessor_util.calculatePositionArrayByTime_1M(_thetime['hour'], _thetime['minute'])
            position2M_str = DataProcessor_util.calculatePositionArrayByTime_2M(_thetime['hour'], _thetime['minute'])

            errormessage_list, last_ID, n1 = self.__processLastID_tickList(_ticklistDict['ticklist_ID'], errormessage_list)

            errormessage_list, n2 = self.__processLast1H_tickList(_ticklistDict['ticklist_P1H'], errormessage_list)

            errormessage_list, n3 = self.__processLast2M_tickList(_ticklistDict['ticklist_P2M'], position1M_str, position2M_str, errormessage_list)

            total = n1 + n2 + n3
            self.logger.debug("Number of Ticks Processed: " + str(total))

            errormessage_list = self._process_InstantSpeed_vol(_ticklistDict['ticklist_P1H'], _thetime, errormessage_list)
            self.logger.debug('Volume Instant speed calculated')

            self._calculateAverages(position1M_str, position2M_str, errormessage_list)
            self.logger.debug('Averages calculates')

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++do Processing ticks Error: ' + repr(ex)
            errormessage_list.append(errormessage)

        self.logger.info('***Method->doProcess tick list ENDS')
        return errormessage_list, last_ID
    #fin doProcess
#class
