#!/usr/bin/env python
""" Common File
    Variables Constantes con las querys Mariadb Sql.
    
    @author Alfredo Sanz
    @date Agosto 2017
"""
#APIs imports

TABLE_NAME_TICKS_BACKUP = 'trading_db.ticks_fibex_bckp_'
TABLE_NAME_TICKS_BACKUP_DEC_EUROFX = 'trading_db.zbckp_ticks_feuro'
TABLE_NAME_TICKS_BACKUP_DEC_SP500 = 'trading_db.zbckp_ticks_fsp500'
TABLE_NAME_TICKS_BACKUP_DEC_NASDAQ = 'trading_db.zbckp_ticks_fnasdaq'
TABLE_NAME_TICKS_BACKUP_DEC_BUND   = 'trading_db.zbckp_ticks_fnasdaq'

CREATE_TABLE_BACKUP_TICKS_01 =      'CREATE TABLE IF NOT EXISTS '+ TABLE_NAME_TICKS_BACKUP

CREATE_TABLE_BACKUP_TICKS_02 =      """(
                                          ID BIGINT(20) UNSIGNED NOT NULL,
                                          tickdate INT(11) UNSIGNED NOT NULL,
                                          ticktime INT(11) UNSIGNED NOT NULL,
                                          tickmili INT(11) UNSIGNED NOT NULL,
                                          ope VARCHAR(8) NOT NULL,
                                          trade_price INT(11) NOT NULL,
                                          trade_vol INT(11) NOT NULL,
                                          buy_price INT(11) NOT NULL,
                                          sell_price INT(11) NOT NULL,
                                          PRIMARY KEY (ID)
                                    )
                                    ENGINE = INNODB
                                    CHARACTER SET utf8
                                    COLLATE utf8_general_ci
                                    ROW_FORMAT = DYNAMIC;
                                    """

SELECT_INSERT_TICKS_BACKP_01 =      '     INSERT INTO ' + TABLE_NAME_TICKS_BACKUP

SELECT_INSERT_TICKS_BACKP_02 =      """   (ID, tickdate, ticktime, tickmili, ope, trade_price, trade_vol, buy_price, sell_price) 
                                          SELECT ID, 
                                                tickdate, 
                                                ticktime, 
                                                tickmili,
                                                ope, 
                                                trade_price, 
                                                trade_vol, 
                                                buy_price, 
                                                sell_price 
                                          FROM trading_db.ticks_fibex
                                          ORDER BY ID ASC
                                    """


DELETE_TICKS_BY_SESION =            """   DELETE FROM trading_db.ticks_fibex WHERE tickdate=%s """


CREATE_TABLE_BACKUP_TICKS_DEC_EUROFX_01 =  'CREATE TABLE IF NOT EXISTS ' + TABLE_NAME_TICKS_BACKUP_DEC_EUROFX + '_'
CREATE_TABLE_BACKUP_TICKS_DEC_EUROFX_02 = """                                          
                                          (
                                          ID BIGINT(20) UNSIGNED NOT NULL,
                                          tickdate INT(11) UNSIGNED NOT NULL,
                                          ticktime INT(11) UNSIGNED NOT NULL,
                                          tickmili INT(11) UNSIGNED NOT NULL,
                                          ope VARCHAR(8) NOT NULL,
                                          trade_price DECIMAL(6,5) NOT NULL,
                                          trade_vol INT(11) NOT NULL,
                                          buy_price DECIMAL(6,5)  NOT NULL,
                                          sell_price DECIMAL(6,5)  NOT NULL,
                                          PRIMARY KEY (ID)
                                    )
                                    ENGINE = INNODB
                                    CHARACTER SET utf8
                                    COLLATE utf8_general_ci
                                    ROW_FORMAT = DYNAMIC;
                                    """

SELECT_INSERT_TICKS_BACKP_DEC_EUROFX_01 =   'INSERT INTO ' + TABLE_NAME_TICKS_BACKUP_DEC_EUROFX + '_'
SELECT_INSERT_TICKS_BACKP_DEC_EUROFX_02 =   """ (ID, tickdate, ticktime, tickmili, ope, trade_price, trade_vol, buy_price, sell_price) 
                                                SELECT ID, 
                                                      tickdate, 
                                                      ticktime, 
                                                      tickmili,
                                                      ope, 
                                                      trade_price, 
                                                      trade_vol, 
                                                      buy_price, 
                                                      sell_price 
                                                FROM trading_db.ticks_feuro
                                                ORDER BY ID ASC
                                          """


DELETE_TICKS_BY_SESION_DEC_EUROFX =       'DELETE FROM trading_db.ticks_feuro WHERE tickdate=%s'
DELETE_TICKS_DEC_EUROFX =       'DELETE FROM trading_db.ticks_feuro'


CREATE_TABLE_BACKUP_TICKS_DEC_SP500_01 =  'CREATE TABLE IF NOT EXISTS ' + TABLE_NAME_TICKS_BACKUP_DEC_SP500 + '_'
CREATE_TABLE_BACKUP_TICKS_DEC_SP500_02 = """                                          
                                          (
                                          ID BIGINT(20) UNSIGNED NOT NULL,
                                          tickdate INT(11) UNSIGNED NOT NULL,
                                          ticktime INT(11) UNSIGNED NOT NULL,
                                          tickmili INT(11) UNSIGNED NOT NULL,
                                          ope VARCHAR(8) NOT NULL,
                                          trade_price DECIMAL(6,2) NOT NULL,
                                          trade_vol INT(11) NOT NULL,
                                          buy_price DECIMAL(7,2)  NOT NULL,
                                          sell_price DECIMAL(7,2)  NOT NULL,
                                          PRIMARY KEY (ID)
                                    )
                                    ENGINE = INNODB
                                    CHARACTER SET utf8
                                    COLLATE utf8_general_ci
                                    ROW_FORMAT = DYNAMIC;
                                    """

SELECT_INSERT_TICKS_BACKP_DEC_SP500_01 =   'INSERT INTO ' + TABLE_NAME_TICKS_BACKUP_DEC_SP500 + '_'
SELECT_INSERT_TICKS_BACKP_DEC_SP500_02 =   """ (ID, tickdate, ticktime, tickmili, ope, trade_price, trade_vol, buy_price, sell_price) 
                                                SELECT ID, 
                                                      tickdate, 
                                                      ticktime, 
                                                      tickmili,
                                                      ope, 
                                                      trade_price, 
                                                      trade_vol, 
                                                      buy_price, 
                                                      sell_price 
                                                FROM trading_db.ticks_fsp500
                                                ORDER BY ID ASC
                                          """


DELETE_TICKS_BY_SESION_DEC_SP500 =            'DELETE FROM trading_db.ticks_fsp500 WHERE tickdate=%s '
DELETE_TICKS_DEC_SP500 =            'DELETE FROM trading_db.ticks_fsp500 '


CREATE_TABLE_BACKUP_TICKS_DEC_BUND_01 =  'CREATE TABLE IF NOT EXISTS ' + TABLE_NAME_TICKS_BACKUP_DEC_BUND + '_'
CREATE_TABLE_BACKUP_TICKS_DEC_BUND_02 = """                                          
                                          (
                                          ID BIGINT(20) UNSIGNED NOT NULL,
                                          tickdate INT(11) UNSIGNED NOT NULL,
                                          ticktime INT(11) UNSIGNED NOT NULL,
                                          tickmili INT(11) UNSIGNED NOT NULL,
                                          ope VARCHAR(8) NOT NULL,
                                          trade_price DECIMAL(6,2) NOT NULL,
                                          trade_vol INT(11) NOT NULL,
                                          buy_price DECIMAL(7,2)  NOT NULL,
                                          sell_price DECIMAL(7,2)  NOT NULL,
                                          PRIMARY KEY (ID)
                                    )
                                    ENGINE = INNODB
                                    CHARACTER SET utf8
                                    COLLATE utf8_general_ci
                                    ROW_FORMAT = DYNAMIC;
                                    """

SELECT_INSERT_TICKS_BACKP_DEC_BUND_01 =   'INSERT INTO ' + TABLE_NAME_TICKS_BACKUP_DEC_BUND + '_'
SELECT_INSERT_TICKS_BACKP_DEC_BUND_02 =   """ (ID, tickdate, ticktime, tickmili, ope, trade_price, trade_vol, buy_price, sell_price) 
                                                SELECT ID, 
                                                      tickdate, 
                                                      ticktime, 
                                                      tickmili,
                                                      ope, 
                                                      trade_price, 
                                                      trade_vol, 
                                                      buy_price, 
                                                      sell_price 
                                                FROM trading_db.ticks_bund
                                                ORDER BY ID ASC
                                          """


DELETE_TICKS_BY_SESION_DEC_BUND =   'DELETE FROM trading_db.ticks_bund WHERE tickdate=%s '
DELETE_TICKS_DEC_BUND =             'DELETE FROM trading_db.ticks_bund '


CREATE_TABLE_BACKUP_TICKS_DEC_NASDAQ_01 =  'CREATE TABLE IF NOT EXISTS ' + TABLE_NAME_TICKS_BACKUP_DEC_NASDAQ + '_'
CREATE_TABLE_BACKUP_TICKS_DEC_NASDAQ__02 = """                                          
                                          (
                                          ID BIGINT(20) UNSIGNED NOT NULL,
                                          tickdate INT(11) UNSIGNED NOT NULL,
                                          ticktime INT(11) UNSIGNED NOT NULL,
                                          tickmili INT(11) UNSIGNED NOT NULL,
                                          ope VARCHAR(8) NOT NULL,
                                          trade_price DECIMAL(6,2) NOT NULL,
                                          trade_vol INT(11) NOT NULL,
                                          buy_price DECIMAL(7,2)  NOT NULL,
                                          sell_price DECIMAL(7,2)  NOT NULL,
                                          PRIMARY KEY (ID)
                                    )
                                    ENGINE = INNODB
                                    CHARACTER SET utf8
                                    COLLATE utf8_general_ci
                                    ROW_FORMAT = DYNAMIC;
                                    """

SELECT_INSERT_TICKS_BACKP_DEC_NASDAQ__01 =   'INSERT INTO ' + TABLE_NAME_TICKS_BACKUP_DEC_NASDAQ + '_'
SELECT_INSERT_TICKS_BACKP_DEC_NASDAQ__02 =   """ (ID, tickdate, ticktime, tickmili, ope, trade_price, trade_vol, buy_price, sell_price) 
                                                SELECT ID, 
                                                      tickdate, 
                                                      ticktime, 
                                                      tickmili,
                                                      ope, 
                                                      trade_price, 
                                                      trade_vol, 
                                                      buy_price, 
                                                      sell_price 
                                                FROM trading_db.ticks_fnasdaq
                                                ORDER BY ID ASC
                                          """


DELETE_TICKS_BY_SESION_DEC_NASDAQ =            'DELETE FROM trading_db.ticks_fnasdaq WHERE tickdate=%s '
DELETE_TICKS_DEC_NASDAQ =            'DELETE FROM trading_db.ticks_fnasdaq '
DELETE_TICKS_DEC_DAX =            'DELETE FROM trading_db.ticks_dax '




DELETE_VISU_CALCULATED_DATA_EUROFX =       'DELETE FROM trading_db.visu_datacalc_feuro'

DELETE_VISU_CALCULATED_DATA_SP500 =        'DELETE FROM trading_db.visu_datacalc_fsp500'

DELETE_VISU_CALCULATED_DATA_BUND =        'DELETE FROM trading_db.visu_datacalc_bund'

DELETE_VISU_CALCULATED_DATA_NASDAQ =       'DELETE FROM trading_db.visu_datacalc_fnasdaq'

DELETE_VISU_CALCULATED_DATA_DAX =       'DELETE FROM trading_db.visu_datacalc_dax'



GET_TICKS_BY_SESION_LIST =          """   SELECT ID,
                                                tickdate,
                                                ticktime,
                                                tickmili, 
                                                ope,
                                                trade_price,
                                                trade_vol,
                                                buy_price,
                                                sell_price
                                          FROM trading_db.ticks_fibex
                                          WHERE tickdate=%s
                                          ORDER BY ID ASC   
                                    """


GET_LAST_TICKS_BY_ID_LIST =         """   SELECT ID,
                                                tickdate,
                                                ticktime,
                                                tickmili, 
                                                ope,
                                                trade_price,
                                                trade_vol,
                                                buy_price,
                                                sell_price
                                          FROM trading_db.ticks_fibex
                                          WHERE tickdate=%s AND
                                                ID >%s
                                          ORDER BY ID ASC      
                                    """


GET_TICKS_LAST_1H =                 """   SELECT ID,
                                                tickdate,
                                                ticktime,
                                                tickmili, 
                                                ope,
                                                trade_price,
                                                trade_vol,
                                                buy_price,
                                                sell_price
                                          FROM trading_db.ticks_fibex
                                          WHERE tickdate=%s AND
                                                ticktime >= %s
                                          ORDER BY ID ASC      
                                    """

GET_CURRENT_PRICES =                """   SELECT tickdate,
                                                ticktime,
                                                tickmili, 
                                                buy_price,
                                                sell_price
                                          FROM trading_db.prices_fibex
                                          WHERE tickdate=%s
                                    """


GET_SESSION_LIST =                  """   SELECT DISTINCT(tickdate) as tickdate
                                          FROM trading_db.ticks_fibex                               
                                          ORDER BY tickdate ASC      
                                    """

GET_CURRENT_PRICES_EUROFX =         """   SELECT tickdate,
                                                ticktime,
                                                tickmili, 
                                                buy_price,
                                                sell_price
                                          FROM trading_db.prices_feuro
                                          WHERE tickdate=%s
                                    """

GET_CURRENT_PRICES_SP500 =          """   SELECT tickdate,
                                                ticktime,
                                                tickmili, 
                                                buy_price,
                                                sell_price
                                          FROM trading_db.prices_fsp500
                                          WHERE tickdate=%s
                                    """

GET_CURRENT_PRICES_BUND =          """   SELECT tickdate,
                                                ticktime,
                                                tickmili, 
                                                buy_price,
                                                sell_price
                                          FROM trading_db.prices_bund
                                          WHERE tickdate=%s
                                    """


GET_CURRENT_PRICES_NASDAQ =         """   SELECT tickdate,
                                                ticktime,
                                                tickmili, 
                                                buy_price,
                                                sell_price
                                          FROM trading_db.prices_fnasdaq
                                          WHERE tickdate=%s
                                    """

GET_CURRENT_PRICES_DAX =            """   SELECT tickdate,
                                                ticktime,
                                                tickmili, 
                                                buy_price,
                                                sell_price
                                          FROM trading_db.prices_dax
                                          WHERE tickdate=%s
                                    """


GET_SESSION_LIST_EUROFX =           """   SELECT DISTINCT(tickdate) as tickdate
                                          FROM trading_db.ticks_feuro
                                          ORDER BY tickdate ASC      
                                    """


GET_SESSION_LIST_SP500 =            """   SELECT DISTINCT(tickdate) as tickdate
                                          FROM trading_db.ticks_fsp500
                                          ORDER BY tickdate ASC      
                                    """

GET_SESSION_LIST_BUND =            """   SELECT DISTINCT(tickdate) as tickdate
                                          FROM trading_db.ticks_bund
                                          ORDER BY tickdate ASC      
                                    """

GET_SESSION_LIST_NASDAQ =           """   SELECT DISTINCT(tickdate) as tickdate
                                          FROM trading_db.ticks_fnasdaq 
                                          ORDER BY tickdate ASC      
                                    """

GET_SESSION_LIST_DAX =              """   SELECT DISTINCT(tickdate) as tickdate
                                          FROM trading_db.ticks_dax 
                                          ORDER BY tickdate ASC      
                                    """

GET_LAST_TICKS_BY_ID_LIST_EUROFX =  """   SELECT ID,
                                                tickdate,
                                                ticktime,
                                                tickmili, 
                                                ope,
                                                trade_price,
                                                trade_vol,
                                                buy_price,
                                                sell_price
                                          FROM trading_db.ticks_feuro
                                          WHERE tickdate=%s AND
                                                ID >%s
                                          ORDER BY ID ASC      
                                    """


GET_LAST_TICKS_BY_ID_LIST_SP500 =   """   SELECT ID,
                                                tickdate,
                                                ticktime,
                                                tickmili, 
                                                ope,
                                                trade_price,
                                                trade_vol,
                                                buy_price,
                                                sell_price
                                          FROM trading_db.ticks_fsp500
                                          WHERE tickdate=%s AND
                                                ID >%s
                                          ORDER BY ID ASC      
                                    """

GET_LAST_TICKS_BY_ID_LIST_BUND =   """   SELECT ID,
                                                tickdate,
                                                ticktime,
                                                tickmili, 
                                                ope,
                                                trade_price,
                                                trade_vol,
                                                buy_price,
                                                sell_price
                                          FROM trading_db.ticks_bund
                                          WHERE tickdate=%s AND
                                                ID >%s
                                          ORDER BY ID ASC      
                                    """

GET_LAST_TICKS_BY_ID_LIST_NASDAQ =  """   SELECT ID,
                                                tickdate,
                                                ticktime,
                                                tickmili, 
                                                ope,
                                                trade_price,
                                                trade_vol,
                                                buy_price,
                                                sell_price
                                          FROM trading_db.ticks_fnasdaq
                                          WHERE tickdate=%s AND
                                                ID >%s
                                          ORDER BY ID ASC      
                                    """

GET_LAST_TICKS_BY_ID_LIST_DAX =     """   SELECT ID,
                                                tickdate,
                                                ticktime,
                                                tickmili, 
                                                ope,
                                                trade_price,
                                                trade_vol,
                                                buy_price,
                                                sell_price
                                          FROM trading_db.ticks_dax
                                          WHERE tickdate=%s AND
                                                ID >%s
                                          ORDER BY ID ASC      
                                    """


SQL_INSERT_UPDATE_GLOBAL_DATA =     """   INSERT INTO trading_db.visu_global 
                                          (sessiondate, market, buy_price, sell_price, vprofile, volume_total, speed) 
                                          VALUES(%s, %s, %s, %s, %s, %s, %s) 
                                          ON DUPLICATE KEY UPDATE 
                                          sessiondate=VALUES(sessiondate), market=VALUES(market), buy_price=VALUES(buy_price), 
                                          sell_price=VALUES(sell_price), vprofile=VALUES(vprofile), volume_total=VALUES(volume_total),
                                          speed=VALUES(speed)                                          
                                    """

SQL_INSERT_UPDATE_CALCULATED_DATA_EUROFX =      """   INSERT INTO trading_db.visu_datacalc_feuro 
                                                      (sessiondate, candle_id, delta, vol_avg, delta_strong, data03, data04, data05, data06
                                                      , data07, data08)
                                                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                                                      ON DUPLICATE KEY UPDATE 
                                                      sessiondate=VALUES(sessiondate), candle_id=VALUES(candle_id), delta=VALUES(delta), 
                                                      vol_avg=VALUES(vol_avg), delta_strong=VALUES(delta_strong), data03=VALUES(data03),
                                                      data04=VALUES(data04), data05=VALUES(data05), data06=VALUES(data06)
                                                      , data07=VALUES(data07), data08=VALUES(data08)
                                                      
                                                """

SQL_INSERT_UPDATE_CALCULATED_DATA_SP500 =      """   INSERT INTO trading_db.visu_datacalc_fsp500 
                                                      (sessiondate, candle_id, delta, vol_avg, delta_strong, data03, data04, data05, data06
                                                      , data07, data08)
                                                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  
                                                      ON DUPLICATE KEY UPDATE 
                                                      sessiondate=VALUES(sessiondate), candle_id=VALUES(candle_id), delta=VALUES(delta), 
                                                      vol_avg=VALUES(vol_avg), delta_strong=VALUES(delta_strong), data03=VALUES(data03),
                                                      data04=VALUES(data04), data05=VALUES(data05), data06=VALUES(data06)
                                                      , data07=VALUES(data07), data08=VALUES(data08)
                                                """

SQL_INSERT_UPDATE_CALCULATED_DATA_BUND =      """   INSERT INTO trading_db.visu_datacalc_bund 
                                                      (sessiondate, candle_id, delta, vol_avg, delta_strong, data03, data04, data05, data06
                                                      , data07, data08)
                                                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  
                                                      ON DUPLICATE KEY UPDATE 
                                                      sessiondate=VALUES(sessiondate), candle_id=VALUES(candle_id), delta=VALUES(delta), 
                                                      vol_avg=VALUES(vol_avg), delta_strong=VALUES(delta_strong), data03=VALUES(data03),
                                                      data04=VALUES(data04), data05=VALUES(data05), data06=VALUES(data06)
                                                      , data07=VALUES(data07), data08=VALUES(data08)
                                                """


SQL_INSERT_UPDATE_CALCULATED_DATA_NASDAQ =      """   INSERT INTO trading_db.visu_datacalc_fnasdaq 
                                                      (sessiondate, candle_id, delta, vol_avg, delta_strong, data03, data04, data05, data06
                                                      , data07, data08)
                                                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                                                      ON DUPLICATE KEY UPDATE 
                                                      sessiondate=VALUES(sessiondate), candle_id=VALUES(candle_id), delta=VALUES(delta), 
                                                      vol_avg=VALUES(vol_avg), delta_strong=VALUES(delta_strong), data03=VALUES(data03),
                                                      data04=VALUES(data04), data05=VALUES(data05), data06=VALUES(data06)
                                                      , data07=VALUES(data07), data08=VALUES(data08)
                                                """


SQL_INSERT_UPDATE_CALCULATED_DATA_DAX =         """   INSERT INTO trading_db.visu_datacalc_dax 
                                                      (sessiondate, candle_id, delta, vol_avg, delta_strong, data03, data04, data05, data06
                                                      , data07, data08)
                                                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                                                      ON DUPLICATE KEY UPDATE 
                                                      sessiondate=VALUES(sessiondate), candle_id=VALUES(candle_id), delta=VALUES(delta), 
                                                      vol_avg=VALUES(vol_avg), delta_strong=VALUES(delta_strong), data03=VALUES(data03),
                                                      data04=VALUES(data04), data05=VALUES(data05), data06=VALUES(data06)
                                                      , data07=VALUES(data07), data08=VALUES(data08)
                                                """