#!/usr/bin/env python
""" Common File
    Variables Constantes
    
    @author Alfredo Sanz
    @date Febrero 2017
    @update Sept 2020
"""
#APIs imports


TIME_UNIT_MILI = 'MILISECOND'
TIME_UNIT_SEC  = 'S'
TIME_UNIT_MIN  = 'M'

TIME_LOOP_TOSLEEP = 0.5

#Intervalo de tiempo para enviar datos al Servidor - en milisegundos
TIME_INTERVAL_SEND_DATA_SERVER_MILISECONDS = 900
TIME_INTERVAL_SEND_VPROFILE_DATA_SERVER_MILISECONDS = 9000

TWO_MINUTES_IN_SECONDS = 120


TICK_OPE_BUY    = 'BUY'
TICK_OPE_SELL   = 'SELL'
TICK_OPE_PRICE  = 'PRICE'


MONGO_HOST = "mongodb://127.0.0.1:27017"
MYSQL_HOST = 'host="127.0.0.1'
             
MONGO_DATABASE_IBEX35 = "DB-IBEX35"
MONGO_COLLECTION_IBEX_TICKS = "TICKS"
        
MARKET_EUROFX   =   "EUROFX"
MARKET_SP500    =   "SP500"    
MARKET_NASDAQ   =   "NASDAQ"
MARKET_DAX      =   "DAX"
MARKET_CL       =   "CL"


WEB_URL_EXPLORE_LOCALHOST               = "http://localhost:8080/etda/api/v1/explore"
WEB_URL_EXPLORE_HOST                    = "https://eltradingdealf.appspot.com/etda/api/v1/explore"

WEB_URL_DATA_IBEX_LOCALHOST             = "http://localhost:8080/etda/api/v1/ibex/data"
WEB_URL_DATA_IBEX_HOST                  = "https://eltradingdealf.appspot.com/etda/api/v1/ibex/data"

WEB_URL_DATA_VPROFILE_LOCALHOST         = "https://localhost:8080/etda/api/v1/ibex/datavp"
WEB_URL_DATA_VPROFILE_HOST              = "https://eltradingdealf.appspot.com/etda/api/v1/ibex/datavp"

WEB_URL_GET_SESSIONS_IBEX_LOCALHOST     = "http://localhost:8080/etda/api/v1/ibex/sessions"
WEB_URL_GET_SESSIONS_IBEX_HOST          = "https://eltradingdealf.appspot.com/etda/api/v1/ibex/sessions"

WEB_URL_DELETE_SESSION_IBEX_LOCALHOST   = "http://localhost:8080/etda/api/v1/ibex/session/"
WEB_URL_DELETE_SESSION_IBEX_HOST        = "https://eltradingdealf.appspot.com/etda/api/v1/ibex/session/"

WEB_MARKET_IBEX = 'IBEX35'


#---------CALENDAR----------
INIT_TRADING_TIME_HOUR      = 8
FINISH_TRADING_TIME_HOUR    = 22

INIT_TRADING_TIME_HOUR_INTEGER      = 80000

HOUR_BACKUP_SESSIONS        = 7

#--------TICK CANDLE SETUP------------
TICKS_BY_CANDLE = {"EUROFX": 75, "SP500": 90, "NASDAQ": 75, "DAX": 45, "CL": 75}

VOL_FILTER_TRESHOLD = {"EUROFX": 10, "SP500": 25, "NASDAQ": 25, "DAX": 4, "CL": 10}



