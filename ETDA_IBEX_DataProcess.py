#!/usr/bin/env python
""" Proceso principal para el procesamiento de
    los datos del Ibex35

    -Obtiene datos de la BD
    -Calcula datos
    -Envia datos calculados a GAE para la web

    @author Alfredo Sanz
    @date Febrero 2017
"""

#APIs imports
import logging
import logging.config
import time
from decimal import *

#local imports
from StopProcessCondition import StopProcessConditionSingleton
#from dao.Ibex_mongo_Dao import Ibex_mongo_Dao
from dao.Ibex_mysql_Dao import Ibex_mysql_Dao
from dataprocess.DataProcessor_ibex import DataProcessor_ibex
from model.Singleton_DataTemp import Singleton_DataTemp
from common import Util
from common import Constantes
from common import MyCalendar
from restclient.RestDIO_ibex import RestDIO_Ibex 
from model.Ibex_data import Ibex_data

class ETDA_ibex_DataProcess:

    dataSingleton = Singleton_DataTemp()
    spc = StopProcessConditionSingleton()

    isTradingON = False

    #Global errors Lists
    ge_getticks_errormessage_list = []
    ge_procestick_errormessage_list = []
    ge_senddata_errormessage_list = []
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
    * @return errormessage, dict{'tick_id_list','ticklist_P1H','ticklist_P2M' | List}
    """
    def __getTickListsFromDB(self, _last_tick_id, _curTimeInDate, _curDatetime):

        self.logger.info('***Method->__getTickListsFromDB INIT')

        errormessage1 = '0'
        errormessage2 = '0'
        errormessage  = '0'
        result = {}
        #dao = Ibex_mongo_Dao()
        dao_mysql = Ibex_mysql_Dao()

        #TICK LIST SINCE LAST QUERY
        try:
            errormessage1, tick_id_list = dao_mysql.getListTicks_LastByID(_last_tick_id, _curTimeInDate)
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
            errormessage = errormessage + ' - ' + '++--++Error In IBEX-35 __getTickListsFromDB LAST-ID: ' + repr(ex)
        #


        #TICK LIST UP LAST 1 HOUR
        try:
            time_up_1h_int = Util.getCurrentHourTimeMinusMinutes(_curDatetime, '1H')
            #errormessage2, tick_p1h_list = dao.getListTicks_Last1H(_curTimeInDate, time_up_1h_int)
            errormessage2, tick_p1h_list = dao_mysql.getListTicks_Last1H(_curTimeInDate, time_up_1h_int)
            if '0' == errormessage2:
                result['ticklist_P1H'] = tick_p1h_list
            else:
                result['ticklist_P1H'] = []

                if '0' == errormessage:
                    errormessage = errormessage2
                else:
                    errormessage = errormessage + ' - ' + errormessage2
                #
            #

            self.logger.debug('           __getTickListsFromDB, ticklist_P1H ENDS, list len: ' + str(len(result['ticklist_P1H'])))

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = errormessage + ' - ' + '++--++Error In IBEX-35 __getTickListsFromDB LAST-1H: ' + repr(ex)
        #


        #TICK LIST UP LAST 2 MINUTES
        #los ultimos dos minutos los cogemos de la lista de la ultima hora
        try:
            time_up_2m_int = Util.getCurrentHourTimeMinusMinutes(_curDatetime, '2M')
            tick_p2m_list = []
            for tick in result['ticklist_P1H']:

                #la lista de 1H no esta ordenada.
                #Cogemos solo los registros que sean mas recientes de 2M
                if tick.time >= time_up_2m_int:
                    tick_p2m_list.append(tick)
                #
            #for            
            result['ticklist_P2M'] = tick_p2m_list

            self.logger.info('           __getTickListsFromDB, ticklist_P2M ENDS, list len: ' + str(len(result['ticklist_P2M'])))

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage  = errormessage + ' - ' + '++--++Error In IBEX-35 __getTickListsFromDB LAST-2M: ' + repr(ex)
        #

        self.logger.info('***Method->__getTickListsFromDB ENDS')
        return errormessage, result
    #fin __getTickListsFromDB



    def __updateCurrentPrices(self, _curTimeInDate):
        
        try:
            dao_mysql = Ibex_mysql_Dao()
            errormessage, prices_dict = dao_mysql.getPrices_current(_curTimeInDate)

            ibxData = self.dataSingleton.ibexData
            ibxData.current_buy_price = prices_dict['buy_price']
            ibxData.current_sell_price = prices_dict['sell_price']

            self.logger.info('           __updateCurrentPrices, Current prices updated: buy=' + str(prices_dict['buy_price']) + ', sell=' + str(prices_dict['sell_price']))

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = errormessage + ' - ' + '++--++Error In IBEX-35 __updateCurrentPrices: ' + repr(ex)
        #
    #fin __updateCurrentPrices



    def __printErrors(self, _errormessage, _getTicksErrorMsgList, _processTicksErrorMsgList, _sendDataErrorMesgList, _generalErrorMesgList, _copy):

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

        if 0 < len(_sendDataErrorMesgList):
            i = 1
            for mes in _sendDataErrorMesgList:
                self.logger.info("final senData error (" +str(i)+"): " +  str(mes))
                i += 1
            #

            if _copy:
                self.ge_senddata_errormessage_list.append(_sendDataErrorMesgList)
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
        _sendDataErrorMesgList[:] = []
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



    def __doBackupAndDelete(self):

        self.logger.info("***Method->Backup and Delete INIT")

        #dao = Ibex_mongo_Dao()
        dao_mysql = Ibex_mysql_Dao()
        dio = RestDIO_Ibex()

        errormessage, sesion_list = dao_mysql.getSessions()
        if '0' != errormessage:
            self.logger.info("Error getting Database Session list for backup: " + errormessage)
            return
        #

        for sesion in sesion_list:
            #backup DB local
            errormessage = dao_mysql.backupSession(sesion)
            if '0' != errormessage:
                self.logger.info("Error Backing up Session in local Database: " + errormessage)
            #

            #delete datastore
            errormessage2 = dio.deleteSession(sesion)
            if '0' != errormessage2:
                self.logger.info("Error Deleting Session in datastore: " + errormessage2)
            #
        #for

        #ZERO for acumulated fields
        ibxData = self.dataSingleton.ibexData
        ibxData.setZeroAcumulatedFields()

        self.logger.info("***Method->Backup and Delete ENDS")
    #fin __doBackupAndDelete



    def __checkCalendar(self):

        hourofday = Util.getHourOfDay()
        self.logger.info('hourofday===================' + str(hourofday))
        
        current_calendar_key = Util.getCurrentCalendarKey()
        self.logger.info('current_calendar_key========' + current_calendar_key)
        today_calendar = MyCalendar.thecalendar_ibex35[current_calendar_key]
        self.logger.info('today_calendar==============' + repr(today_calendar))
        
        """
        today_calendar [openmarket str<Y/N/F>, 
                        openmarket hour  int<h>, 
                        closemarket hour int<h>],
                        backup_done int<0/1>
        """

        #CHECKING OPEN MARKET
        if 'S' == today_calendar[0]:
            self.logger.info('today_calendar[0]==============S')
            if hourofday >= today_calendar[1] and hourofday < today_calendar[2]:

                self.logger.info('today_calendar[1]==============S')    
                self.isTradingON = True
            else:
                self.logger.info('today_calendar[1]==============N')   
                self.isTradingON = False
            #
        else:
            self.logger.info('today_calendar[0]==============N')
            self.isTradingON = False
        #

        #MAKE BACKUP
        if 'S' == today_calendar[0]:
            self.logger.info('today_calendar[0],BCKUP========S')
            if hourofday == 7:
                self.logger.info('hourofday===============H=7')
                if 0 == today_calendar[3]:
                    self.logger.info('today_calendar[3]==============dobackup')
                    errormessage = self.__doBackupAndDelete()
                    today_calendar[3] = 1
                #
            #
        #
    #fin __checkCalendar



    """
    * Metodo principal del proceso
    *
    * Tiene el algoritmo principal del proceso para recoger
    * los datos y calcular información y enviarla a GAE para la web
    *
    * Es un bucle sin fin que se para con CTRL-C en la consola
    """
    def dowork(self):

        self.logger.debug('***Flag de StopProcessConditionSingleton es: %s', str(self.spc.stopProcessFlag))
        self.logger.info('***dowork INIT')

        errormessage = '0'
        getTicksErrorMsgList = []
        processTicksErrorMsgList = []
        sendDataErrorMesgList = []
        generalErrorMesgList = []

        opcount = 0
        lastSendTime  = Util.getCurrentTime(self.logger).get('dtdt')
        lastResetTimeInSec2PM   = 0 #formato int
        lastResetTimeInSec1PH   = 0 #formato int
        last_tick_id = '0'
        deliveryID = Util.generateDateTimeBasedKey()  #id que se usara para el registro de datos que se envia a Host
        
        lastSendTime_vp = Util.getCurrentTime(self.logger).get('dtdt')
        deliveryID_vp = Util.generateDateTimeBasedKey()  #id que se usara para el registro de datos que se envia a Host

        dio = RestDIO_Ibex()
        dap = DataProcessor_ibex()

        #--++--MAIN PROCESS LOOP
        while False == self.spc.stopProcessFlag:

            try:
                #Check Conditions for Loop Exit
                _check = self.__checkExitConditions()
                if _check:
                    break
                #

                #check Calendar, Ensuring that we are within Open market hours
                self.__checkCalendar()
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
                errMesgGetTicks, ticklistDict = self.__getTickListsFromDB(last_tick_id, thetime['intDate'], thetime['dtdt'])
                if '0' != errMesgGetTicks:
                    getTicksErrorMsgList.append(errMesgGetTicks)

                    continue
                #
                self.logger.info('***LOOP*** **TIME TRAP: QUERY DB ends')



                #--++--PROCESS TICKS LIST
                processTicksErrorMsgListOrig, last_tick_id_tmp = dap.doProcess(ticklistDict, thetime)
                if 0 < len(processTicksErrorMsgListOrig):
                    processTicksErrorMsgList.append(processTicksErrorMsgListOrig)
                #
                #Puede que en la iteracion no hubiese ticks nuevos, y el tickID vendra a '0'
                if '0' != last_tick_id_tmp:
                    last_tick_id = last_tick_id_tmp
                else:
                    #Si no ha habido nuevos Ticks, actualizamos el precio actual.
                    self.__updateCurrentPrices(thetime['intDate'])
                #
                self.logger.info('***LOOP*** **TIME TRAP: PROCESS DATA('+str(last_tick_id)+') ends')



                #--++--SENDING DATA TO SERVER
                difMiliseconds = Util.diffTimesMilliseconds(thetime['dtdt'], lastSendTime, self.logger)
                self.logger.info('***LOOP*** *DIFF: ' + str(difMiliseconds) + ', comp=' + str(Constantes.TIME_INTERVAL_SEND_DATA_SERVER_MILISECONDS <= difMiliseconds))

                #Send global data
                if Constantes.TIME_INTERVAL_SEND_DATA_SERVER_MILISECONDS <= difMiliseconds:
                    lastSendTime = thetime['dtdt']

                    #--++--
                    deliveryID += 1
                    errMesgSendData = dio.sendData(self.dataSingleton.ibexData, deliveryID, thetime['intDate'],  thetime['intTime'], thetime, opcount)
                    opcount += 1
                    if '0' != errMesgSendData:
                        sendDataErrorMesgList.append(errMesgSendData) #Si hubo error lo archivamos
                    #
                    self.logger.info('***LOOP*** **TIME TRAP: SEND DATA ends')
                #if


                #Send Volume profile data
                difMiliseconds_vp = Util.diffTimesMilliseconds(thetime['dtdt'], lastSendTime_vp, self.logger)
                self.logger.info('***LOOP*** *DIFF: ' + str(difMiliseconds_vp) + ', comp=' + str(Constantes.TIME_INTERVAL_SEND_VPROFILE_DATA_SERVER_MILISECONDS <= difMiliseconds_vp))

                if Constantes.TIME_INTERVAL_SEND_VPROFILE_DATA_SERVER_MILISECONDS <= difMiliseconds_vp:
                    lastSendTime_vp = thetime['dtdt']

                    #--++--
                    deliveryID_vp += 1
                    errMesgSendVprofileData = dio.sendVProfileData(self.dataSingleton.ibexData, deliveryID, thetime['intDate'],  thetime['intTime'], thetime, opcount)                    
                    self.dataSingleton.ibexData.setZeroTmpVolumeProfile()
                    if '0' != errMesgSendVprofileData:
                        sendDataErrorMesgList.append(errMesgSendVprofileData) #Si hubo error lo archivamos
                    #
                    self.logger.info('***LOOP*** **TIME TRAP: SEND VPROFILE DATA ends')
                #if

                self.logger.info('***LOOP*** **TIME TRAP: ITERATION ends')

            except Exception as ex:
                self.logger.error(repr(ex.args))
                self.logger.exception(ex)
                generalErrorMesgList.append('++--++Error In IBEX-35 Main Loop: ' + repr(ex))

            #imprime los errores de esta iteracion y vacia cada lista de errores para la siguiente
            self.__printErrors(errormessage, getTicksErrorMsgList, processTicksErrorMsgList, sendDataErrorMesgList, generalErrorMesgList, True)
        #while

        self.__printErrors(errormessage, ge_getticks_errormessage_list, ge_procestick_errormessage_list, ge_senddata_errormessage_list, self.ge_general_errormessage_list, False)

        self.logger.info('***dowork ENDS')
    #fin dowork
#class
