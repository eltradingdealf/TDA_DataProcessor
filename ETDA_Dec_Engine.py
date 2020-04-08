#!/usr/bin/env python
""" Proceso principal para el procesamiento de
    los datos del futuro del Euro. CME market.

    -Obtiene datos de la BD
    -Calcula datos
    -Guarda o envía los datos calculados para su consumo por
    otro soft.

    @author Alfredo Sanz
    @date Marzo 2019
"""

#APIs imports
import logging
import logging.config
import time
from decimal import *

#local imports
from StopProcessCondition import StopProcessConditionSingleton
from dao.Dec_mysql_Dao import Dec_mysql_Dao
from dataprocess.DataProcessor_dec import DataProcessor_dec
from model.Singleton_DataTemp_Dec import Singleton_DataTemp_Dec
from common import Util
from common import Constantes
from common import MyCalendar
from model.Dec_data import Dec_data

class ETDA_Dec_Engine:

    dataSingleton = Singleton_DataTemp_Dec()
    spc = StopProcessConditionSingleton()

    isTradingON = False

    #Global errors Lists
    ge_getticks_errormessage_list = []
    ge_procestick_errormessage_list = []
    ge_general_errormessage_list = []

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
    * Obtiene de la BD las diferentes listas de datos que
    * habra que procesar.
    *
    * @return errormessage, dict{'tick_id_list' | List}
    """
    def __getTickListsFromDB(self, _last_tick_id, _curTimeInDate, _curDatetime, _market):
        """ errormessage, result[ticklist_ID] with the Tick's List"""
        self.logger.info('***Method->__getTickListsFromDB '+_market+' INIT')

        errormessage1 = '0'
        errormessage2 = '0'
        errormessage  = '0'
        result = {}
        dao_mysql = Dec_mysql_Dao()

        #TICK LIST AFTER LAST QUERY EXECUTION
        try:
            errormessage1, tick_id_list = dao_mysql.getListTicks_LastByID(_last_tick_id, _curTimeInDate, _market)
            if '0' == errormessage1:
                result['ticklist_ID'] = tick_id_list
            else:
                result['ticklist_ID'] = []
                errormessage = errormessage1
            #

            self.logger.debug('           __getTickListsFromDB, _last_tick_id ENDS, list len: ' + str(len(result['ticklist_ID'])))

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = errormessage + ' - ' + '++--++Error In  '+_market+' __getTickListsFromDB LAST-ID: ' + repr(ex)
        #

        self.logger.info('***Method->__getTickListsFromDB '+_market+' ENDS')
        return errormessage, result
    #fin __getTickListsFromDB



    def __updateCurrentPrices(self, _curTimeInDate, _market):
        
        self.logger.info('***Method->__updateCurrentPrices '+_market+' INIT')

        try:
            dao_mysql = Dec_mysql_Dao()
            errormessage, prices_dict = dao_mysql.getPrices_current(_curTimeInDate, _market)

            decData = self.dataSingleton.decData
            decData.current_buy_price = Decimal(prices_dict['buy_price'])
            decData.current_sell_price = Decimal(prices_dict['sell_price'])

            self.logger.info('           __updateCurrentPrices, Current prices updated: buy=' + str(prices_dict['buy_price']) + ', sell=' + str(prices_dict['sell_price']))

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = errormessage + ' - ' + '++--++Error In Decimal future  '+_market+'  __updateCurrentPrices: ' + repr(ex)
        #

        self.logger.info('***Method->__updateCurrentPrices '+_market+' ENDS')
    #fin __updateCurrentPrices



    
    def __printErrors(self, _errormessage, _getTicksErrorMsgList, _processTicksErrorMsgList,  _generalErrorMesgList, _copy):

        if '0' != _errormessage:
            self.logger.debug("Exiting Process with errors: " + _errormessage)
        #

        if 0 < len(_getTicksErrorMsgList):
            i = 1
            for mes in _getTicksErrorMsgList:
                self.logger.info("final getTicks error (" +str(i)+"): " +  str(mes))
                i += 1
            #
            if _copy:
                self.ge_getticks_errormessage_list.append(_getTicksErrorMsgList)           
            #
        #

        if 0 < len(_processTicksErrorMsgList):
            i = 1
            for mes in _processTicksErrorMsgList:
                self.logger.info("final processTicks error (" +str(i)+"): " + str(mes))
                i += 1
            #

            if _copy:
                self.ge_procestick_errormessage_list.append(_processTicksErrorMsgList)    
            #
        #

        if 0 < len(_generalErrorMesgList):
            i = 1
            for mes in _generalErrorMesgList:
                self.logger.info("final General error (" +str(i)+"): " +  str(mes))
                i += 1
            #

            if _copy:
                self.ge_general_errormessage_list.append(_generalErrorMesgList)
            #
        #

        _getTicksErrorMsgList[:] = []
        _processTicksErrorMsgList[:] = []
        _generalErrorMesgList[:] = []
    #fin printErrors



    def __checkExitConditions(self):

        #Exit by Flag
        if True == self.spc.stopProcessFlag:
            return True
        #

        #Exit by Errors
        """
        total_err = len(self.ge_getticks_errormessage_list) + len(self.ge_procestick_errormessage_list) + len(self.ge_senddata_errormessage_list) + len(self.ge_general_errormessage_list)
        if 50 <= total_err:
            logging.info("Too many errors: " + str(total_err))
            #sendMessage()
            #return True
        #
        """
        return False
    #fin __checkExitConditions



    def __doBackupAndDelete(self, _market):

        self.logger.info('***Method->Backup and Delete '+_market+' INIT')

        dao_mysql = Dec_mysql_Dao()

        errormessage, sesion_list = dao_mysql.getSessions(_market)
        if '0' != errormessage:
            self.logger.info('Error getting Database Session list for backup  '+_market+' : ' + errormessage)
            return
        #

        for sesion in sesion_list:
            #backup DB local
            errormessage = dao_mysql.backupSession(sesion, _market)
            if '0' != errormessage:
                self.logger.info('Error Backing up Session in local Database  '+_market+' : ' + errormessage)
            #
        #for

        #ZERO for acumulated fields
        decData = self.dataSingleton.decData
        decData.setZeroAcumulatedFields()

        self.logger.info('***Method->Backup and Delete '+_market+' ENDS')
    #fin __doBackupAndDelete



    def __checkCalendar(self, _market):

        hourofday = Util.getHourOfDay()
        self.logger.debug('hourofday===================' + str(hourofday))
        
        current_calendar_key = Util.getCurrentCalendarKey()
        self.logger.debug('current_calendar_key========' + current_calendar_key)
        today_calendar = MyCalendar.thecalendar_FuturesCME[current_calendar_key]
        self.logger.info('today_calendar==============' + repr(today_calendar))
        
        """
        today_calendar [openmarket str<Y/N/F>, 
                        openmarket hour  int<h>, 
                        closemarket hour int<h>],
                        backup_done int<0/1>
        """

        #CHECKING OPEN MARKET
        if 'S' == today_calendar[0]:
            self.logger.debug('today_calendar[0]==============S')
            if hourofday >= today_calendar[1] and hourofday < today_calendar[2]:

                self.logger.debug('today_calendar[1]==============S')    
                self.isTradingON = True
            else:
                self.logger.debug('today_calendar[1]==============N')   
                self.isTradingON = False
            #
        else:
            self.logger.debug('today_calendar[0]==============N')
            self.isTradingON = False
        #

        #MAKE BACKUP
        if 'S' == today_calendar[0]:
            self.logger.debug('today_calendar[0],BCKUP========S')
            if 0 == today_calendar[3]:
                self.logger.debug('today_calendar[3]==============dobackup')
                errormessage = self.__doBackupAndDelete(_market)
                today_calendar[3] = 1
            #
        #
    #fin __checkCalendar



    
    """
    * Metodo principal del proceso
    *
    * Tiene el algoritmo principal del proceso para recoger
    * los datos y calcular información y almacenarla para su uso
    * por otro software.
    *
    * Es un bucle sin fin que se para con CTRL-C en la consola
    """
    def dowork(self, _market):

        self.logger.debug('***Flag de StopProcessConditionSingleton es: %s', str(self.spc.stopProcessFlag))
        self.logger.info('***dowork '+_market+' INIT')

        errormessage = '0'
        getTicksErrorMsgList = []
        processTicksErrorMsgList = []        
        generalErrorMesgList = []
        
        last_tick_id = '0'
        deliveryID = Util.generateDateTimeBasedKey()  #id que se usara para el registro de datos        
        deliveryID_vp = Util.generateDateTimeBasedKey()  #id que se usara para el registro de datos

        dao_mysql = Dec_mysql_Dao()

        dap = DataProcessor_dec()
        decData = self.dataSingleton.decData
        calculatedData_index_last = 0

        #--++--MAIN PROCESS LOOP
        while False == self.spc.stopProcessFlag:

            try:
                #Check Conditions for Loop Exit
                _check = self.__checkExitConditions()
                if _check:
                    break
                #

                #check Calendar, Ensuring that we are within Open market hours
                self.__checkCalendar(_market)
                if False == self.isTradingON:
                    self.logger.info('***LOOP*** Trading ON: False, wait 60 sec')
                    time.sleep(60)
                    opcount = 0

                    continue
                #

               

                #INIT ITERATION WAITING A TIME'S INTERVAL
                self.logger.info('***LOOP*** INIT ITERATION, Awaiting 0.5 secs')
                time.sleep(Constantes.TIME_LOOP_TOSLEEP)
                self.logger.info('***LOOP*** ITERATION STARTED')

                thetime = Util.getCurrentTime_months(self.logger)



                #--++--GET TICK LIST FROM BROKER MESSAGE DATABASE
                errMesgGetTicks, ticklistDict = self.__getTickListsFromDB(last_tick_id, thetime['intDate'], thetime['dtdt'], _market)
                if '0' != errMesgGetTicks:
                    getTicksErrorMsgList.append(errMesgGetTicks)

                    continue
                #
                self.logger.info('***LOOP*** **TIME TRAP: QUERY DB ends')



                #--++--PROCESS TICKS LIST
                processTicksErrorMsgListOrig, last_tick_id_tmp = dap.doProcess(ticklistDict, thetime, _market)
                if 0 < len(processTicksErrorMsgListOrig):
                    processTicksErrorMsgList.append(processTicksErrorMsgListOrig)
                #
                #Puede que en la iteracion no hubiese ticks nuevos, y el tickID vendra a '0'
                if '0' != last_tick_id_tmp:
                    last_tick_id = last_tick_id_tmp
                else:
                    #Si no ha habido nuevos Ticks, actualizamos el precio actual.
                    self.__updateCurrentPrices(thetime['intDate'], _market)
                #
                self.logger.info('***LOOP*** **TIME TRAP: PROCESS DATA('+str(last_tick_id)+') ends')

              

                #STORE CALCULATED DATA INTO BROKER DATABASE                
                self.logger.info('***LOOP***  **TIME TRAP **STORING CALCULATED DATA(calculatedData_index_last:'+str(calculatedData_index_last)+', decData.calculatedData_index:'+str(decData.calculatedData_index)+') init')
                while calculatedData_index_last <= decData.calculatedData_index:

                    dao_mysql.updateCalculatedData(_market, decData.calculatedData_ndArray, calculatedData_index_last, thetime)
                    
                    if calculatedData_index_last == decData.calculatedData_index:
                        break
                    elif calculatedData_index_last < decData.calculatedData_index:
                        calculatedData_index_last += 1
                    #
                #
                self.logger.debug('***LOOP***  **TIME TRAP **STORING CALCULATED DATA(calculatedData_index_last:'+str(calculatedData_index_last)+', decData.calculatedData_index:'+str(decData.calculatedData_index)+') ends')
                


                #STORE GLOBAL DATA INTO BROKER DATABASE
                dao_mysql.updateGlobalData(_market, decData, thetime)
                self.logger.debug('***LOOP***  **TIME TRAP **STORING GLOBAL DATA ends')


                 
                self.logger.info('***LOOP*** **TIME TRAP: ITERATION ends')

            except Exception as ex:
                self.logger.error(repr(ex.args))
                self.logger.exception(ex)
                generalErrorMesgList.append('++--++Error In Dec '+_market+' Main Loop: ' + repr(ex))

            #imprime los errores de esta iteracion y vacia cada lista de errores para la siguiente
            self.__printErrors(errormessage, getTicksErrorMsgList, processTicksErrorMsgList, generalErrorMesgList, True)
        #while

        self.__printErrors(errormessage, ge_getticks_errormessage_list, ge_procestick_errormessage_list, self.ge_general_errormessage_list, False)

        self.logger.info('***dowork '+_market+' ENDS')
    #fin dowork
#fin clase