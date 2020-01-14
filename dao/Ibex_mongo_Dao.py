#!/usr/bin/env python
""" Clase para operar contra MongoDB en relacion
    a datos del F-Ibex

    @author Alfredo Sanz
    @date Febrero 2017
"""

#APIs imports
import logging
import logging.config
import time
from decimal import *
import pymongo
from pymongo import MongoClient
from bson.son import SON

#local imports
from dataprocess.DataProcessor import DataProcessor
from dao.IbexDao import IbexDAO
from model.Tick_ibex import Tick_ibex
from common import Util
from common import Constantes



class Ibex_mongo_Dao(IbexDAO):


    
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

        try:
            client = MongoClient(Constantes.MONGO_HOST)
            db = client[Constantes.MONGO_DATABASE_IBEX35]
            coll = db[Constantes.MONGO_COLLECTION_IBEX_TICKS]

            self.logger.debug("mongoQuery LAST_ID-> date:" + str(_curTimeInDate) + ", ID:" + str(_lastTick_id))
            self.logger.info('=====find_ID trap before find')
            cursor = coll.find({"$and":[{"date":_curTimeInDate},{"ID":{"$gt":_lastTick_id}}]},{"_id":0}).sort([("ID", pymongo.ASCENDING)])
            self.logger.info('=====find_ID trap after find:')

            for doc in cursor:
                tick = Tick_ibex()

                tick.ID                      = doc['ID']
                tick.date                    = doc['date']
                tick.time                    = doc['time']
                tick.ope                     = str(doc['ope'])
                tick.trade_price             = doc['trade_price']
                tick.trade_vol               = doc['trade_vol']
                tick.buy_price               = doc['buy_price']
                tick.sell_price              = doc['sell_price']

                result.append(tick)
                self.logger.debug('Tick: ' + str(tick))
            #
            self.logger.info('=====find_ID trap after For:'+ str(len(result)))

        except Exception as ex:
            self.logger.error("Error Getting tick list from Mongo", ex)
            errormessage = "Error Getting tick list from Mongo: " + repr(ex)

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

        try:
            client = MongoClient(Constantes.MONGO_HOST)
            db = client[Constantes.MONGO_DATABASE_IBEX35]
            coll = db[Constantes.MONGO_COLLECTION_IBEX_TICKS]

            self.logger.info('mongoQuery LAST P1H-> date:' + str(_curTimeInDate))
            self.logger.info('mongoQuery LAST P1H-> hour:' + str(_time1H_ago))

            self.logger.info('=====find_1H trap before find')
            cursor = coll.find({"$and":[{"date":_curTimeInDate},{"time":{"$gte":_time1H_ago}}]},{"_id":0}).sort([("ID", pymongo.ASCENDING)])
            #cursor = coll.find({"$and":[{"date":_curTimeInDate},{"time":{"$gte":_time1H_ago}}]},{"_id":0}).sort([("time", pymongo.ASCENDING)])

            self.logger.info('=====find_1H trap after find')
            for doc in cursor:
                tick = Tick_ibex()

                tick.ID                      = doc['ID']
                tick.date                    = doc['date']
                tick.time                    = doc['time']
                tick.ope                     = str(doc['ope'])
                tick.trade_price             = doc['trade_price']
                tick.trade_vol               = doc['trade_vol']
                tick.buy_price               = doc['buy_price']
                tick.sell_price              = doc['sell_price']

                result.append(tick)
                self.logger.debug('Tick: ' + str(tick))
            #
            self.logger.info('=====find_1H trap after For:'+ str(len(result)))

        except Exception as ex:
            self.logger.error("Error Getting tick list(LAST-1H) from Mongo", ex)
            errormessage = "Error Getting tick list(LAST-1H) from Mongo: " + repr(ex)

        self.logger.info('***Method->Dao-ibex->Getting tick list(LAST-1H)('+str(len(result))+') ENDS')
        return errormessage, result
    #fin getListTicks_Last1H



    """
    * Query all the Ticks from the last 1 Hour.
    * **********Use Aggregation framework.*************
    * Esta lista de registros no esta ordenada.
    *
    * @param _curTimeInDate int con la fecha actual. Fecha actual == session actual
    * @param _time1H_ago int con la hora actual(hhmmss) - 1 hora
    *
    * @return List<Tick_ibex> de ticks con datos del Ibex35 SIN Ordenar.
    """
    def getListTicks_Last1H_aggregation(self, _curTimeInDate, _time1H_ago):
        """ errormessage, result [Tick_ibex] --> todos los ticks desde la ultima hora 
            Using Aggregation Framework. Sin Ordenar."""

        self.logger.info('***Method->Dao-ibex->Getting (aggregation) tick list(LAST-1H) INIT')

        errormessage = '0'
        result = []

        try:
            client = MongoClient(Constantes.MONGO_HOST)
            db = client[Constantes.MONGO_DATABASE_IBEX35]
            coll = db[Constantes.MONGO_COLLECTION_IBEX_TICKS]

            self.logger.info('mongoQuery LAST P1H-> date:' + str(_curTimeInDate))
            self.logger.info('mongoQuery LAST P1H-> hour:' + str(_time1H_ago))
            self.logger.info('=====find_1H (aggreg) trap before command')

            pipeline = [
                        {"$match":{"$and":[{"date":_curTimeInDate},{"time":{"$gte":_time1H_ago}}]}}#,
                        #{"$sort": SON([("ID", 1)])}
            ]
            
            tick_db = db.command('aggregate', Constantes.MONGO_COLLECTION_IBEX_TICKS, pipeline=pipeline, explain=False)  #explain=True)
            #self.logger.info(repr(tick_db))  for explain outputs
            tick_list = tick_db['result']

            self.logger.info('=====find_1H (aggreg) trap after command:' + str(len(tick_db['result'])))
            for doc in tick_list:
                tick = Tick_ibex()

                tick.ID                      = doc['ID']
                tick.date                    = doc['date']
                tick.time                    = doc['time']
                tick.ope                     = str(doc['ope'])
                tick.trade_price             = doc['trade_price']
                tick.trade_vol               = doc['trade_vol']
                tick.buy_price               = doc['buy_price']
                tick.sell_price              = doc['sell_price']

                result.append(tick)
                self.logger.debug('Tick: ' + str(tick))
            #

            self.logger.info('=====find_1H (aggreg) trap after For:'+ str(len(result)))

        except Exception as ex:
            self.logger.error("Error Getting (aggregation) tick list(LAST-1H) from Mongo", ex)
            errormessage = "Error Getting (aggregation) tick list(LAST-1H) from Mongo: " + repr(ex)

        self.logger.info('***Method->Dao-ibex->Getting (aggregation) tick list(LAST-1H)('+str(len(result))+') ENDS')
        return errormessage, result
    #fin getListTicks_Last1H


    """
    * Query all the Ticks from the last 2 Minutes.
    *
    * @param _curTimeInDate int con la fecha actual. Fecha actual == session actual
    *
    * @return List<Tick_ibex> de ticks con datos del Ibex35 ordenada por ts.
    """
    def getListTicks_Last2M(self, _curTimeInDate, _time2M_ago):
        """ errormessage, result [Tick_ibex] --> todos los ticks desde los ultimos 2 minutos """

        self.logger.debug('***Method->Dao-ibex->Getting tick list(LAST-2M) INIT')

        errormessage = '0'
        result = []

        try:
            client = MongoClient(Constantes.MONGO_HOST)
            db = client[Constantes.MONGO_DATABASE_IBEX35]
            coll = db[Constantes.MONGO_COLLECTION_IBEX_TICKS]

            self.logger.debug("mongoQuery LAST P2M-> date:" + str(_curTimeInDate))
            cursor = coll.find({"$and":[{"date":_curTimeInDate},{"time":{"$gte":_time2M_ago}}]},{"_id":0}).sort([("ID", pymongo.ASCENDING)])

            for doc in cursor:
                tick = Tick_ibex()

                tick.ID                      = doc['ID']
                tick.date                    = doc['date']
                tick.time                    = doc['time']
                tick.ope                     = str(doc['ope'])
                tick.trade_price             = doc['trade_price']
                tick.trade_vol               = doc['trade_vol']
                tick.buy_price               = doc['buy_price']
                tick.sell_price              = doc['sell_price']

                result.append(tick)
                self.logger.debug('Tick: ' + str(tick))
            #

        except Exception as ex:
            self.logger.error("Error Getting tick list(LAST-2M) from Mongo", ex)
            errormessage = "Error Getting tick list(LAST-2M) from Mongo: " + repr(ex)

        self.logger.info('***Method->Dao-ibex->Getting tick list(LAST-2M)('+str(len(result))+') ENDS')
        return errormessage, result
    #fin getListTicks_Last2M



    """
    * Obtiene una lista de sesiones presentes en la Coleccion TICKS de Mongodb.
    *
    * @return list[int] con las sesiones.
    """
    def getSessions(self):

        self.logger.info('***Method->Dao-ibex->getSessions INIT')

        errormessage = '0'
        result = []

        try:
            client = MongoClient(Constantes.MONGO_HOST)
            db = client[Constantes.MONGO_DATABASE_IBEX35]
            coll = db[Constantes.MONGO_COLLECTION_IBEX_TICKS]

            cursor = coll.distinct("date")

            for sess in cursor:
                result.append(sess)
            #

        except Exception as ex:
            self.logger.error("Error Getting Session_ibex list from Mongo", ex)
            errormessage = "Error Getting Session_ibex list from Mongo: " + repr(ex)

        self.logger.info('***Method->Dao-ibex->getSessions ('+repr(result)+') ENDS')

        return errormessage, result
    #fin getSessions



    """
    * Hace el backup de los datos de una sesion en Mongodb y los elimina
    * de la coleccion principal.
    *
    * @param _idSesion La sesion que queremos copiar y guardar.
    """
    def backupSession(self, _idSesion):

        self.logger.info('***Method->backupSession INIT')

        errormessage = '0'
        result = []
        
        try:
            client = MongoClient(Constantes.MONGO_HOST)
            db = client[Constantes.MONGO_DATABASE_IBEX35]
            coll = db[Constantes.MONGO_COLLECTION_IBEX_TICKS]
            coll2 = db[Constantes.MONGO_COLLECTION_IBEX_TICKS + '_backup_' + str(_idSesion)]
            
            cursor = coll.find({"date":_idSesion}).sort([("ID", pymongo.ASCENDING)])
            
            i = 0
            for doc in cursor:
                coll2.insert_one(doc)
                i += 1
            #
            self.logger.info(str(i) + " docs copied.")

            coll.delete_many({"date":_idSesion})
            self.logger.info("docs many deleted from TICKS.")

        except Exception as ex:
            self.logger.error("Error createBackupTICKS_ibex from Mongo", ex)
            errormessage = "Error createBackupTICKS_ibex from Mongo: " + repr(ex)

        self.logger.info('***Method->backupSession ENDS')
        return errormessage
    #fin backupSession
#class
