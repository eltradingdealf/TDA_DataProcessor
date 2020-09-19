#!/usr/bin/env python
""" Clase para operar contra BD en relacion
    a datos de futuros con precios en formato decimal.

    @author Alfredo Sanz
    @date Marzo 2019
    @update Sept 2020
"""

#APIs imports
import logging
import logging.config
import time
from decimal import *
import numpy as np
import pymysql

#local imports
from dataprocess.DataProcessor import DataProcessor
from dao.iDecDao import iDecDAO
from model.Dec_data import Dec_data
from model.Tick_Dec import Tick_Dec
from common import Util
from common import Constantes
from common import query_sql
import ConfigRoot



class Dec_mysql_Dao(iDecDAO):


    
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
    * Obtiene de la Base de datos los precios actuales.
    *
    * @return errormessage, result <dict>{int, int}
    """
    def getPrices_current(self, _curTimeInDate, _market):
        """ return result {'buy_price, 'sell_price'} """

        self.logger.info("***Method->Dao-Dec->Getting prices Current "+ _market + " INIT")

        errormessage = '0'
        result = {'sell_price':'0.0', 'buy_price':'0.0'}
        connection = None

        self.logger.info('=====mysql, mysql_Query Current_prices-> date:' + str(_curTimeInDate))

        try:
            self.logger.debug('=====mysql, CurrentPrices trap before conn')
            connection = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user=ConfigRoot.db_mariadb_user,
                                         passwd=ConfigRoot.db_mariadb_pass,
                                         db="trading_db",
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
                                         
            self.logger.debug('=====mysql, CurrentPrices trap after conn')

            with connection.cursor() as cursor:
                sql = ''
                if Constantes.MARKET_EUROFX == _market:
                    sql = query_sql.GET_CURRENT_PRICES_EUROFX
                elif Constantes.MARKET_SP500 == _market:
                    sql = query_sql.GET_CURRENT_PRICES_SP500
                elif Constantes.MARKET_NASDAQ == _market:
                    sql = query_sql.GET_CURRENT_PRICES_NASDAQ
                elif Constantes.MARKET_DAX == _market:
                    sql = query_sql.GET_CURRENT_PRICES_DAX
                #

                cursor.execute(sql, (_curTimeInDate))
                self.logger.debug('=====mysql, CurrentPrices trap after execute')
                rs = cursor.fetchall()
                self.logger.debug('=====mysql, CurrentPrices trap after cursor')
                for row in rs:
                    result['sell_price']  = str(row['buy_price'])   #porque en bd estan al reves
                    result['buy_price']   = str(row['sell_price'])  #porque en bd estan al reves
                #
            #
            self.logger.debug('=====mysql, find_ID trap after recolect')


        except Exception as ex:
            self.logger.error("Error Getting current prices from MariaDB  "+ _market, ex)
            errormessage = "Error Getting current from MariaDB  "+ _market + " : " + repr(ex)
        finally:
            if connection:
                connection.close()
            #
        #

        self.logger.info('***Method->Dao-Dec->Getting prices Current '+ _market + '  ENDS')
        return errormessage, result
    #fin getPrices_current



    """
    * Obtiene la lista de ticks aniadidos desde la
    * ultima consulta. El parametro indica el ultimo
    * tick obtenido en la consulta anterior.
    *
    * @param _lastTick_id string con el id del ultimo tick recuperado
    * @param _curTimeInDate int con la fecha actual. Fecha actual == session actual
    *                           Por si acaso alguna vez se nos olvida borrar los datos 
    *                           de la session anterior.
    *
    * @return List<Tick_Dec> de ticks con datos del Futuro pertinente ordenada por ts.
    """
    def getListTicks_LastByID(self, _lastTick_id, _curTimeInDate, _market):
        """ errormessage, result [Tick_Dec] --> todos los ticks desde el ultimo """

        self.logger.info("***Method->Dao-dec->Getting tick list(LAST-ID) INIT")

        errormessage = '0'
        result = []
        connection = None

        self.logger.debug('=====mysql, mysql_Query LAST_ID-> date:' + str(_curTimeInDate))
        self.logger.info('=====mysql, mysql_Query LAST_ID-> _lastTick_id:' + str(_lastTick_id))

        try:
            self.logger.debug('=====mysql, find_ID trap before conn')
            connection = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user=ConfigRoot.db_mariadb_user,
                                         passwd=ConfigRoot.db_mariadb_pass,
                                         db="trading_db",
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
                                         
            self.logger.debug('=====mysql, find_ID trap after conn')

            with connection.cursor() as cursor:
                sql = ''
                if Constantes.MARKET_EUROFX == _market:
                    sql = query_sql.GET_LAST_TICKS_BY_ID_LIST_EUROFX
                elif Constantes.MARKET_SP500 == _market:
                    sql = query_sql.GET_LAST_TICKS_BY_ID_LIST_SP500
                elif Constantes.MARKET_NASDAQ == _market:
                    sql = query_sql.GET_LAST_TICKS_BY_ID_LIST_NASDAQ
                elif Constantes.MARKET_DAX == _market:
                    sql = query_sql.GET_LAST_TICKS_BY_ID_LIST_DAX
                #

                cursor.execute(sql, (_curTimeInDate, _lastTick_id))
                self.logger.debug('=====mysql, find_ID trap after execute')
                rs = cursor.fetchall()
                self.logger.debug('=====mysql, find_ID trap after cursor')
                for row in rs:
                    tick = Tick_Dec()

                    tick.ID                      = row['ID']
                    tick.date                    = row['tickdate']
                    tick.time                    = row['ticktime']
                    tick.mili                    = row['tickmili']
                    tick.ope                     = str(row['ope'])
                    tick.trade_price             = str(row['trade_price'])
                    tick.trade_vol               = row['trade_vol']                    
                    tick.buy_price               = str(row['buy_price'])                    
                    tick.sell_price              = str(row['sell_price'])

                    result.append(tick)
                #
            #
            self.logger.debug('=====mysql, find_ID trap after recolect')

        except Exception as ex:
            self.logger.error("Error Getting tick list from MariaDB", ex)
            errormessage = "Error Getting tick list from MariaDB: " + repr(ex)
        finally:
            if connection:
                connection.close()
            #
        #

        self.logger.info('***Method->Dao-ibex->Getting tick list(LAST-ID)('+str(len(result))+') ENDS')
        return errormessage, result
    #fin getListTicks_LastByID



    """
    * Actualiza los datos de la tabla de datos Calculados de volumen
    * para el mercado indicado.
    *
    * @param __market string con el id del mercado
    * @param _calculatedData_ndArray ndArray con todos los datos calculados
    *
    * @return anything.
    """
    def updateCalculatedData(self, __market, _calculatedData_ndArray, _index, _theTime):
        """ update Calculated data table for the market """

        self.logger.info("***Method->Dao-dec->updateCalculatedData INIT " + str(_index))

        errormessage = '0'
        result = []
        connection = None


        try:
            self.logger.debug('=====mysql, SQL_INSERT_UPDATE_CALCULATED_DATA_Fxxx trap before conn')
            connection = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user=ConfigRoot.db_mariadb_user,
                                         passwd=ConfigRoot.db_mariadb_pass,
                                         db="trading_db",
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
                                         
            self.logger.debug('=====mysql, SQL_INSERT_UPDATE_CALCULATED_DATA_Fxxx trap after conn')

            sql = ''
            if Constantes.MARKET_EUROFX == __market:
                sql = query_sql.SQL_INSERT_UPDATE_CALCULATED_DATA_EUROFX
            elif Constantes.MARKET_SP500 == __market:
                sql = query_sql.SQL_INSERT_UPDATE_CALCULATED_DATA_SP500
            elif Constantes.MARKET_NASDAQ == __market:
                sql = query_sql.SQL_INSERT_UPDATE_CALCULATED_DATA_NASDAQ
            elif Constantes.MARKET_DAX == __market:
                sql = query_sql.SQL_INSERT_UPDATE_CALCULATED_DATA_DAX
            #
            
            self.logger.debug('=====mysql, _calculatedData_ndArray=' + repr(_calculatedData_ndArray))

            with connection.cursor() as cursor:
                self.logger.debug('=====mysql, query=' + sql)
                cursor.execute(sql, (_theTime['intDate'], _index,
                                    str(_calculatedData_ndArray[0, _index]),
                                    str(_calculatedData_ndArray[1, _index]),
                                    str(_calculatedData_ndArray[2, _index]),
                                    str(_calculatedData_ndArray[3, _index]),
                                    str(_calculatedData_ndArray[4, _index]),
                                    str(_calculatedData_ndArray[5, _index])))
            #
            self.logger.debug('=====mysql, SQL_INSERT_UPDATE_CALCULATED_DATA_Fxxx query executed')

        except Exception as ex:
            self.logger.error("Error storing calculated data into MariaDB", ex)
            errormessage = "Error storing calculated data into MariaDB: " + repr(ex)
        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #

        self.logger.info("***Method->Dao-dec->updateCalculatedData ENDS")
        return errormessage
    #fin updateCalculatedData




    """
    * Actualiza los datos de la tabla de datos globales
    * para el mercado indicado.
    *
    * @param __market string con el id del mercado
    * @param _decData Dec_data objeto contenedor de los datos calculados por el procesador.
    *
    * @return anything.
    """
    def updateGlobalData(self, _market, _decData, _theTime):
        """ update global data table for the market """

        self.logger.info("***Method->Dao-dec->updateGlobalData INIT")

        errormessage = '0'
        result = []
        connection = None


        try:
            self.logger.debug('=====mysql, SQL_INSERT_UPDATE_GLOBAL_DATA trap before conn')
            connection = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user=ConfigRoot.db_mariadb_user,
                                         passwd=ConfigRoot.db_mariadb_pass,
                                         db="trading_db",
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
                                         
            self.logger.debug('=====mysql, SQL_INSERT_UPDATE_GLOBAL_DATA trap after conn')

            #cursor = connection.cursor()
            with connection.cursor() as cursor:
                cursor.execute(query_sql.SQL_INSERT_UPDATE_GLOBAL_DATA, (_theTime['intDate'],
                                                                         _market, str(_decData.current_buy_price),
                                                                         str(_decData.current_sell_price),
                                                                         '0',
                                                                         _decData.total_vol_sess,
                                                                         _decData.speedCurrent))
            #
            self.logger.debug('=====mysql, SQL_INSERT_UPDATE_GLOBAL_DATA query executed')

        except Exception as ex:
            self.logger.error("Error storing global data into MariaDB", ex)
            errormessage = "Error storing global data into MariaDB: " + repr(ex)
        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #

        self.logger.info("***Method->Dao-dec->updateGlobalData ENDS")
        return errormessage
    #fin updateGlobalData



    """
    * Obtiene una lista de sesiones presentes en la Coleccion TICKS de MariaDB.
    *
    * @return list[int] con las sesiones.
    """
    def getSessions(self, _market):
        """ errormessage, result[int] --> todas sesiones """

        self.logger.info('***Method->Dao-Dec->getSessions  '+ _market + ' INIT')

        errormessage = '0'
        result = []
        connection = None

        try:
            connection = pymysql.connect(host="127.0.0.1",
                                        port=3306,
                                        user=ConfigRoot.db_mariadb_user,
                                        passwd=ConfigRoot.db_mariadb_pass,
                                        db="trading_db",
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
                                        
            with connection.cursor() as cursor:
                sql = ''
                if Constantes.MARKET_EUROFX == _market:
                    sql = query_sql.GET_SESSION_LIST_EUROFX
                elif Constantes.MARKET_SP500 == _market:
                    sql = query_sql.GET_SESSION_LIST_SP500
                elif Constantes.MARKET_NASDAQ == _market:
                    sql = query_sql.GET_SESSION_LIST_NASDAQ
                elif Constantes.MARKET_DAX == _market:
                    sql = query_sql.GET_SESSION_LIST_DAX
                #

                cursor.execute(sql)
                rs = cursor.fetchall()
                for row in rs:
                    sess = row['tickdate']

                    result.append(sess)
                #
            #

        except Exception as ex:
            self.logger.error("Error Getting session list from MariaDB  "+ _market, ex)
            errormessage = "Error Getting session list from MariaDB  "+ _market + " : " + repr(ex)
        finally:
            if connection:
                connection.close()
            #
        #

        self.logger.info('***Method->Dao-Dec->getSessions('+str(len(result))+')  '+ _market + ' ENDS')
        return errormessage, result
    #fin getSessions



    def blankTables(self, _market):

        self.logger.info('***Method->Dao-ibex->blankTables INIT')

        errormessage = '0'
        result = []
        connection = None

        try:
            self.logger.info('=====mysql, DELETE DATA IN TICKS TABLE FOR MARKET: ' + _market)
            connection = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user=ConfigRoot.db_mariadb_user,
                                         passwd=ConfigRoot.db_mariadb_pass,
                                         db="trading_db",
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            sql_delete = ''
            if Constantes.MARKET_EUROFX == _market:
                sql_delete = query_sql.DELETE_TICKS_DEC_EUROFX
            elif Constantes.MARKET_SP500 == _market:
                sql_delete = query_sql.DELETE_TICKS_DEC_SP500
            elif Constantes.MARKET_NASDAQ == _market:
                sql_delete = query_sql.DELETE_TICKS_DEC_NASDAQ
            elif Constantes.MARKET_DAX == _market:
                sql_delete = query_sql.DELETE_TICKS_DEC_DAX
            #

            cursor2 = connection.cursor()
            cursor2.execute(sql_delete)

            self.logger.info('=====mysql, DELETE TICKS ENDS, query=' + str(sql_delete))

        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #

        try:
            self.logger.info('=====mysql, DELETE DATA IN VISU-DATACALC TABLE FOR MARKET: ' + _market)
            connection = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user=ConfigRoot.db_mariadb_user,
                                         passwd=ConfigRoot.db_mariadb_pass,
                                         db="trading_db",
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            sql_delete_02 = ''
            if Constantes.MARKET_EUROFX == _market:
                sql_delete_02 = query_sql.DELETE_VISU_CALCULATED_DATA_EUROFX
            elif Constantes.MARKET_SP500 == _market:
                sql_delete_02 = query_sql.DELETE_VISU_CALCULATED_DATA_SP500
            elif Constantes.MARKET_NASDAQ == _market:
                sql_delete_02 = query_sql.DELETE_VISU_CALCULATED_DATA_NASDAQ
            elif Constantes.MARKET_DAX == _market:
                sql_delete_02 = query_sql.DELETE_VISU_CALCULATED_DATA_DAX
            #

            cursor2 = connection.cursor()
            cursor2.execute(sql_delete_02)

            self.logger.info('=====mysql, DELETE VISU-DATACALC ENDS, query=' + str(sql_delete_02))

        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #

        self.logger.info('***Method->Dao-Dec->blankTables ENDS')
        return errormessage
    # fin blankTables



    """
    * Hace el backup de las tablas de ticks de las sesiones anteriores,
    * y borra todo de las tablas de visualizacion
    *
    * @param _idSesion La sesion que queremos copiar y guardar.
    """
    def backupSession(self, _idSesion, _market):
        """ errormessage """

        self.logger.info('***Method->Dao-ibex->backupSession INIT')

        errormessage = '0'
        result = []
        connection = None

        try:
            self.logger.info('=====mysql, CREATING NEW BACKUP TABLE FOR MARKET: ' + _market)
            connection = pymysql.connect(host="127.0.0.1",
                                        port=3306,
                                        user=ConfigRoot.db_mariadb_user,
                                        passwd=ConfigRoot.db_mariadb_pass,
                                        db="trading_db",
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
                                        
            query_ct = ''
            if Constantes.MARKET_EUROFX == _market:
                query_ct = query_sql.CREATE_TABLE_BACKUP_TICKS_DEC_EUROFX_01
                query_ct += str(_idSesion)         
                query_ct += query_sql.CREATE_TABLE_BACKUP_TICKS_DEC_EUROFX_02
            elif Constantes.MARKET_SP500 == _market:
                query_ct = query_sql.CREATE_TABLE_BACKUP_TICKS_DEC_SP500_01
                query_ct += str(_idSesion)         
                query_ct += query_sql.CREATE_TABLE_BACKUP_TICKS_DEC_SP500_02
            elif Constantes.MARKET_NASDAQ == _market:
                query_ct = query_sql.CREATE_TABLE_BACKUP_TICKS_DEC_NASDAQ_01
                query_ct += str(_idSesion)         
                query_ct += query_sql.CREATE_TABLE_BACKUP_TICKS_DEC_NASDAQ_02
            #

            cursor = connection.cursor()
            cursor.execute(query_ct)

            self.logger.info('=====mysql, CREATING NEW BACKUP TABLE ENDS, query=' + str(query_ct))

        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #

        try:
            self.logger.info('=====mysql, INSERT SELECT IN THE NEW BACKUP TABLE FOR MARKET: ' + _market)
            connection = pymysql.connect(host="127.0.0.1",
                                        port=3306,
                                        user=ConfigRoot.db_mariadb_user,
                                        passwd=ConfigRoot.db_mariadb_pass,
                                        db="trading_db",
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
                                        
            query_ins_sel = ''
            if Constantes.MARKET_EUROFX == _market:
                query_ins_sel = query_sql.SELECT_INSERT_TICKS_BACKP_DEC_EUROFX_01
                query_ins_sel += str(_idSesion)
                query_ins_sel += query_sql.SELECT_INSERT_TICKS_BACKP_DEC_EUROFX_02
            elif Constantes.MARKET_SP500 == _market:
                query_ins_sel = query_sql.SELECT_INSERT_TICKS_BACKP_DEC_SP500_01
                query_ins_sel += str(_idSesion)
                query_ins_sel += query_sql.SELECT_INSERT_TICKS_BACKP_DEC_SP500_02
            elif Constantes.MARKET_NASDAQ == _market:
                query_ins_sel = query_sql.SELECT_INSERT_TICKS_BACKP_DEC_NASDAQ__01
                query_ins_sel += str(_idSesion)
                query_ins_sel += query_sql.SELECT_INSERT_TICKS_BACKP_DEC_NASDAQ__02
            #        
           
            cursor = connection.cursor()
            cursor.execute(query_ins_sel)

            self.logger.info('=====mysql, INSERT SELECT IN THE NEW BACKUP TABLE ENDS, query=' + str(query_ins_sel))

        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #


        try :
            self.logger.info('=====mysql, DELETE DATA IN TICKS TABLE FOR MARKET: ' + _market)
            connection = pymysql.connect(host="127.0.0.1",
                                        port=3306,
                                        user=ConfigRoot.db_mariadb_user,
                                        passwd=ConfigRoot.db_mariadb_pass,
                                        db="trading_db",
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)

            sql_delete = ''
            if Constantes.MARKET_EUROFX == _market:
                sql_delete = query_sql.DELETE_TICKS_BY_SESION_DEC_EUROFX
            elif Constantes.MARKET_SP500 == _market:
                sql_delete = query_sql.DELETE_TICKS_BY_SESION_DEC_SP500
            elif Constantes.MARKET_NASDAQ == _market:
                sql_delete = query_sql.DELETE_TICKS_BY_SESION_DEC_NASDAQ
            #

            cursor2 = connection.cursor()
            cursor2.execute(sql_delete, _idSesion)

            self.logger.info('=====mysql, DELETE TICKS ENDS, query=' + str(sql_delete))

        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #



        try :
            self.logger.info('=====mysql, DELETE DATA IN VISU-DATACALC TABLE FOR MARKET: ' + _market)
            connection = pymysql.connect(host="127.0.0.1",
                                        port=3306,
                                        user=ConfigRoot.db_mariadb_user,
                                        passwd=ConfigRoot.db_mariadb_pass,
                                        db="trading_db",
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)

            sql_delete_02 = ''
            if Constantes.MARKET_EUROFX == _market:
                sql_delete_02 = query_sql.DELETE_VISU_CALCULATED_DATA_EUROFX
            elif Constantes.MARKET_SP500 == _market:
                sql_delete_02 = query_sql.DELETE_VISU_CALCULATED_DATA_SP500
            elif Constantes.MARKET_NASDAQ == _market:
                sql_delete_02 = query_sql.DELETE_VISU_CALCULATED_DATA_NASDAQ
            #

            cursor2 = connection.cursor()
            cursor2.execute(sql_delete_02)

            self.logger.info('=====mysql, DELETE VISU-DATACALC ENDS, query=' + str(sql_delete_02))

        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #

        self.logger.info('***Method->Dao-Dec->backupSession ENDS')
        return errormessage
    #fin backupSession
#class
