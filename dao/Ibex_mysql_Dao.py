#!/usr/bin/env python
""" Clase para operar contra MongoDB en relacion
    a datos del F-Ibex

    @author Alfredo Sanz
    @date Febrero 2017
    @update Julio 2017
"""

#APIs imports
import logging
import logging.config
import time
from decimal import *
import pymysql
#import sqlalchemy
#from sqlalchemy import create_engine

#local imports
from dataprocess.DataProcessor import DataProcessor
from dao.IbexDao import IbexDAO
from model.Tick_ibex import Tick_ibex
from common import Util
from common import Constantes
from common import query_sql
import ConfigRoot



class Ibex_mysql_Dao(IbexDAO):


    
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
    def getPrices_current(self, _curTimeInDate):
        """ return result {'buy_price, 'sell_price'} """

        self.logger.info("***Method->Dao-ibex->Getting prices Current INIT")

        errormessage = '0'
        result = {}
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
                sql = query_sql.GET_CURRENT_PRICES

                cursor.execute(sql, (_curTimeInDate))
                self.logger.debug('=====mysql, CurrentPrices trap after execute')
                rs = cursor.fetchall()
                self.logger.debug('=====mysql, CurrentPrices trap after cursor')
                for row in rs:
                    result['sell_price']  = row['buy_price']   #porque en bd estan al reves
                    result['buy_price']   = row['sell_price']  #porque en bd estan al reves
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

        self.logger.info('***Method->Dao-ibex->Getting prices Current ENDS')
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
    * @return List<Tick_ibex> de ticks con datos del Ibex35 ordenada por ts.
    """
    def getListTicks_LastByID(self, _lastTick_id, _curTimeInDate):
        """ errormessage, result [Tick_ibex] --> todos los ticks desde el ultimo """

        self.logger.info("***Method->Dao-ibex->Getting tick list(LAST-ID) INIT")

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
                sql = query_sql.GET_LAST_TICKS_BY_ID_LIST

                cursor.execute(sql, (_curTimeInDate, _lastTick_id))
                self.logger.debug('=====mysql, find_ID trap after execute')
                rs = cursor.fetchall()
                self.logger.debug('=====mysql, find_ID trap after cursor')
                for row in rs:
                    tick = Tick_ibex()

                    tick.ID                      = row['ID']
                    tick.date                    = row['tickdate']
                    tick.time                    = row['ticktime']
                    tick.mili                    = row['tickmili']
                    tick.ope                     = str(row['ope'])
                    tick.trade_price             = row['trade_price']
                    tick.trade_vol               = row['trade_vol']
                    tick.buy_price               = row['buy_price']
                    tick.sell_price              = row['sell_price']

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
    * Query all the Ticks from the last 1 Hour
    *
    * @param _curTimeInDate int con la fecha actual. Fecha actual == session actual
    * @param _time1H_ago int con la hora actual(hhmmss) - 1 hora
    *
    * @return List<Tick_ibex> de ticks con datos del Ibex35 ordenada por ts.
    """
    def getListTicks_Last1H(self, _curTimeInDate, _time1H_ago):
        """ errormessage, result [Tick_ibex] --> todos los ticks desde la ultima hora """

        self.logger.info('***Method->Dao-ibex->Getting tick list(LAST-1H) INIT')

        errormessage = '0'
        result = []
        connection = None

        self.logger.debug('=====mysql, mysql_Query LAST P1H-> date:' + str(_curTimeInDate))
        self.logger.debug('=====mysql, mysql_Query LAST P1H-> hour:' + str(_time1H_ago))

        try:
            self.logger.debug('=====mysql, find_1H trap before conn')
            connection = pymysql.connect(host="127.0.0.1",
                                        port=3306,
                                        user=ConfigRoot.db_mariadb_user,
                                        passwd=ConfigRoot.db_mariadb_pass,
                                        db="trading_db",
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
                                        
            self.logger.debug('=====mysql, find_1H trap after conn')

            with connection.cursor() as cursor:
                sql = query_sql.GET_TICKS_LAST_1H

                cursor.execute(sql, (_curTimeInDate, _time1H_ago))
                self.logger.debug('=====mysql, find_1H trap after execute')
                rs = cursor.fetchall()
                self.logger.debug('=====mysql, find_1H trap after cursor')
                for row in rs:
                    tick = Tick_ibex()

                    tick.ID                      = row['ID']
                    tick.date                    = row['tickdate']
                    tick.time                    = row['ticktime']
                    tick.mili                    = row['tickmili']
                    tick.ope                     = str(row['ope'])
                    tick.trade_price             = row['trade_price']
                    tick.trade_vol               = row['trade_vol']
                    tick.buy_price               = row['buy_price']
                    tick.sell_price              = row['sell_price']

                    result.append(tick)
                #
            #
            self.logger.debug('=====mysql, find_1H trap after recolect')

        except Exception as ex:
            self.logger.error("Error Getting tick list from MariaDB", ex)
            errormessage = "Error Getting tick list from MariaDB: " + repr(ex)
        finally:
            if connection:
                connection.close()
            #
        #

        self.logger.info('***Method->Dao-ibex->Getting tick list(LAST-1H)('+str(len(result))+') ENDS')
        return errormessage, result
    #fin getListTicks_Last1H




    def getListTicks_Last1H_aggregation(self, _curTimeInDate, _time1H_ago):
        pass
    #

    """
    * Query all the Ticks from the last 2 Minutes.
    *
    * por ahora no lo vamos a usar
    *
    """
    def getListTicks_Last2M(self, _curTimeInDate, _time2M_ago):
        pass
    #fin getListTicks_Last2M



    """
    * Obtiene una lista de sesiones presentes en la Coleccion TICKS de MariaDB.
    *
    * @return list[int] con las sesiones.
    """
    def getSessions(self):
        """ errormessage, result[int] --> todas sesiones """

        self.logger.info('***Method->Dao-ibex->getSessions INIT')

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
                sql = query_sql.GET_SESSION_LIST

                cursor.execute(sql)
                rs = cursor.fetchall()
                for row in rs:
                    sess = row['tickdate']

                    result.append(sess)
                #
            #

        except Exception as ex:
            self.logger.error("Error Getting session list from MariaDB", ex)
            errormessage = "Error Getting session list from MariaDB: " + repr(ex)
        finally:
            if connection:
                connection.close()
            #
        #

        self.logger.info('***Method->Dao-ibex->*Method->Dao-ibex->getSessions('+str(len(result))+') ENDS')
        return errormessage, result
    #fin getSessions



    """
    * Hace el backup de los datos de una sesion en Mongodb y los elimina
    * de la coleccion principal.
    *
    * @param _idSesion La sesion que queremos copiar y guardar.
    """
    def backupSession(self, _idSesion):
        """ errormessage """

        self.logger.info('***Method->Dao-ibex->backupSession INIT')

        errormessage = '0'
        result = []
        connection = None

        try:
            self.logger.info('=====mysql, CREATING NEW BACKUP TABLE')
            connection = pymysql.connect(host="127.0.0.1",
                                        port=3306,
                                        user=ConfigRoot.db_mariadb_user,
                                        passwd=ConfigRoot.db_mariadb_pass,
                                        db="trading_db",
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
                                        
            query_ct = query_sql.CREATE_TABLE_BACKUP_TICKS_01
            query_ct += str(_idSesion)         
            query_ct += query_sql.CREATE_TABLE_BACKUP_TICKS_02                               
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
            self.logger.info('=====mysql, INSERT SELECT IN THE NEW BACKUP TABLE')
            connection = pymysql.connect(host="127.0.0.1",
                                        port=3306,
                                        user=ConfigRoot.db_mariadb_user,
                                        passwd=ConfigRoot.db_mariadb_pass,
                                        db="trading_db",
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
                                        
            query_ins_sel = query_sql.SELECT_INSERT_TICKS_BACKP_01
            query_ins_sel += str(_idSesion)
            query_ins_sel += query_sql.SELECT_INSERT_TICKS_BACKP_02
            cursor = connection.cursor()
            cursor.execute(query_ins_sel)

            self.logger.info('=====mysql, INSERT SELECT IN THE NEW BACKUP TABLE ENDS, query=' + str(query_ins_sel))

            cursor2 = connection.cursor()
            cursor2.execute(query_sql.DELETE_TICKS_BY_SESION, _idSesion)

            self.logger.info('=====mysql, DELETE TICKS ENDS')

        finally:
            if connection:
                connection.commit()
            #
            if connection:
                connection.close()
            #
        #

        self.logger.info('***Method->Dao-ibex->backupSession ENDS')
        return errormessage
    #fin backupSession
#class
