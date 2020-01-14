import logging
import logging.config
import requests

from common import Constantes
import ConfigRoot

class testapi:


    def __init__(self):
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('PYDACALC')
    #construct



    def testExplore(self):

        self.logger.info("Testing api rest Localhost INIT")

        try:
            resp = requests.get(Constantes.WEB_URL_EXPLORE_LOCALHOST)
        
            self.logger.info("Api reponse: " + repr(resp))
        
        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            listErrorMessage.append('++--++DioSendData Error: ' + repr(ex))

        self.logger.info("Testing api rest Localhost ENDS")

    #fin testExplore



    def testP2M(self):
    
        self.logger.info("Testing P2M api rest Localhost INIT")

        try:
            thedata = {}
            thedata['ID'] = 98457948382
            thedata['date'] = 20170306
            thedata['time'] = 154503
            thedata['market'] = 'IBEX35'
            thedata['current_buy_price'] = 9657
            thedata['current_sell_price'] = 9656
            thedata['total_vol_sess'] = 1024
            thedata['total_buy_vol_sess'] = 1000
            thedata['total_sell_vol_sess'] = 25
            thedata['acum_delta_sess'] = 16.2
            thedata['total_trades_buy_sess'] = 500
            thedata['total_trades_sell_sess'] = 20
            thedata['total_trades_sess'] = 520
            thedata['p2m_vol'] = 100
            thedata['p2m_buy_vol'] = 1500
            thedata['p2m_sell_vol'] = 150
            thedata['p2m_delta'] = 55.8
            thedata['p2m_trades_buy'] = 75
            thedata['p2m_trades_sell'] = 25
            thedata['p2m_trades_total'] = 100
            
            resp = requests.post(Constantes.WEB_URL_DATA2PM_LOCALHOST, 
                                json=thedata,
                                headers={'Content-Type':'application/json'},
                                auth=(ConfigRoot.user, ConfigRoot.pasw))
        



            self.logger.info("Api testP2M reponse: " + repr(resp))
        
        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            listErrorMessage.append('++--++DioSendData Error: ' + repr(ex))

        self.logger.info("Testing P2M api rest Localhost ENDS")
    #fin testP2M
#fin