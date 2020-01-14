#!/usr/bin/env python
""" Clase encargada de interactuar con la
    API REST del servidor para enviar datos
    de Ibex35

    -Envia datos de IBEX35

    @author Alfredo Sanz
    @date Marzo 2017
"""

#APIs imports
import logging
import logging.config
import time
from decimal import *
import requests   #for normal 
import simplejson as json
import threading
import random


#local imports
from model.Singleton_DataTemp import Singleton_DataTemp
from common import Util
from common import Constantes
import ConfigRoot
from restclient import dio_workers

"""
*   DIO: Data Interconnection Object
"""
class RestDIO_Ibex:

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
    * Envia al Servidor GAE los datos calculados de Ibex.
    *
    * PAra no tener que esperar la respuesta del servidor, se crea un proceso
    * que realiza la transaccion entera del envio. 
    *
    * @param _ibex_data Obj con los datos de Ibex a enviar
    * @param _ID string Correspondiente al deliveryID.
    * @param curTimeInDate int con la fecha actual
    * @param curTimeIntime int con la hora/minuto/segundo actual
    * @param _strFechaHora str con la fecha y hora actual.
    * @param _opcount contador de numero de operacion en la sesion
    *
    * @return errormessage str('0') si todo bien, otro valor si hubo algún error
    """
    def sendData(self, _ibex_data, _ID, _curTimeInDate, _curTimeIntime, _thetime, _opcount):

        self.logger.info('***Method->-DIO sendData INIT')

        errormessage = '0'
        pid_int = 0

        try:
            thedata = {}
            thedata['ID'] = _ID
            thedata['opcount'] = _opcount
            thedata['date'] = _curTimeInDate
            thedata['time'] = _curTimeIntime
            thedata['strdatetime'] = _thetime['strFechaHora']
            thedata['strdatetime_mil'] = _thetime['strFechaHora_mil']
            thedata['market'] = Constantes.WEB_MARKET_IBEX
            thedata['current_buy_price']    = _ibex_data.current_buy_price
            thedata['current_sell_price']   = _ibex_data.current_sell_price
            thedata['total_vol_sess']       = _ibex_data.total_vol_sess
            thedata['total_buy_vol_sess']   = _ibex_data.total_buy_vol_sess
            thedata['total_sell_vol_sess']  = _ibex_data.total_sell_vol_sess
            thedata['acum_delta_sess']      = _ibex_data.acum_delta_sess
            thedata['acum_deltaF_sess']      = _ibex_data.acum_deltaF_sess

            thedata['p2mlast_vol']          = _ibex_data.p2mlast_vol
            thedata['p2mlast_buy_vol']      = _ibex_data.p2mlast_buy_vol
            thedata['p2mlast_sell_vol']     = _ibex_data.p2mlast_sell_vol
            thedata['p2mlast_delta']        = _ibex_data.p2mlast_delta
            thedata['p2mlast_deltaF']       = _ibex_data.p2mlast_deltaF
            thedata['p2mlast_deltaF_avg5m'] = _ibex_data.p2mlast_deltaF_avg5m
            thedata['p2mlast_deltaF_avg15m']= _ibex_data.p2mlast_deltaF_avg15m

            thedata['p1hlast_vol']          = _ibex_data.p1hlast_vol
            thedata['p1hlast_buy_vol']      = _ibex_data.p1hlast_buy_vol
            thedata['p1hlast_sell_vol']     = _ibex_data.p1hlast_sell_vol
            thedata['p1hlast_delta']        = _ibex_data.p1hlast_delta
            thedata['p1hlast_deltaF']       = _ibex_data.p1hlast_deltaF

            thedata['instant_speed_buy']    = _ibex_data.instant_speed_vol_buy
            thedata['instant_speed_sell']   = _ibex_data.instant_speed_vol_sell
            thedata['instant_speed_delta']  = _ibex_data.instant_speed_vol_delta

            """
            self.logger.info('DIO - volume_profile_tmp = ' + repr(_ibex_data.tmp_volumeprofile_dict))
            vp_prices_list, vp_volume_list    = _ibex_data.getTmp_volumeprofile_dict_as_list()
            self.logger.info('vp_prices_list=' + vp_prices_list + ', vp_volume_list=' + vp_volume_list)
            thedata['volume_profile_prices']  = vp_prices_list
            thedata['volume_profile_volumes'] = vp_volume_list
            """
            
            self.logger.info('DIO - vpoc_price = ' + str(_ibex_data.vpoc_price))
            self.logger.info('DIO - vpoc_vol = ' + str(_ibex_data.vpoc_vol))
            thedata['vpoc_price']   = _ibex_data.vpoc_price
            thedata['vpoc_vol']     = _ibex_data.vpoc_vol
            
            resp = None

            try:
                self.logger.debug("**Creating dio Thread")
                
                pid_int = random.randint(1, 240)
                t = threading.Thread(target=dio_workers.send_data_ibex35, args=(self.logger,thedata,pid_int, _ID))
                self.logger.debug('dio Thread created. pid=' + str(pid_int))

                t.start()                
                self.logger.debug('dio Thread started. pid=' + str(pid_int))

            except Exception as ex:
                self.logger.info("Error: " + repr(ex))
                #errormessage = "Error"
                self.logger.info('Error HHTP not expected: ' + repr(ex))
            #

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++DioSendData Error: ' + repr(ex)

        self.logger.info('***Method->-DIO sendData ENDS')
        return errormessage
    #fin sendData



    """
    * Envia al Servidor GAE los datos de volume profile.
    *
    * PAra no tener que esperar la respuesta del servidor, se crea un proceso
    * que realiza la transaccion entera del envio. 
    *
    * @param _ibex_data Obj con los datos de Ibex a enviar
    * @param _ID string Correspondiente al deliveryID.
    * @param curTimeInDate int con la fecha actual
    * @param curTimeIntime int con la hora/minuto/segundo actual
    * @param _strFechaHora str con la fecha y hora actual.
    * @param _opcount contador de numero de operacion en la sesion
    *
    * @return errormessage str('0') si todo bien, otro valor si hubo algún error
    """
    def sendVProfileData(self, _ibex_data, _ID, _curTimeInDate, _curTimeIntime, _thetime, _opcount):

        self.logger.info('***Method->-DIO sendVProfileData INIT')

        errormessage = '0'
        pid_int = 0

        try:
            thedata = {}
            thedata['ID'] = _ID
            thedata['opcount'] = _opcount
            thedata['date'] = _curTimeInDate
            thedata['time'] = _curTimeIntime
            thedata['strdatetime'] = _thetime['strFechaHora']
            thedata['strdatetime_mil'] = _thetime['strFechaHora_mil']
            thedata['market'] = Constantes.WEB_MARKET_IBEX
            
            vp_prices_list, vp_volume_list    = _ibex_data.getTmp_volumeprofile_dict_as_list()
            self.logger.info('vp_prices_list=' + vp_prices_list + ', vp_volume_list=' + vp_volume_list)
            thedata['volume_profile_prices']  = vp_prices_list
            thedata['volume_profile_volumes'] = vp_volume_list

            self.logger.info('DIO - vpoc_price = ' + str(_ibex_data.vpoc_price))
            self.logger.info('DIO - vpoc_vol = ' + str(_ibex_data.vpoc_vol))
            thedata['vpoc_price']   = _ibex_data.vpoc_price
            thedata['vpoc_vol']     = _ibex_data.vpoc_vol
            
            resp = None

            try:
                self.logger.debug("**Creating dio Thread")
                
                pid_int = random.randint(1, 240)
                t = threading.Thread(target=dio_workers.send_vprofiledata_ibex35, args=(self.logger,thedata,pid_int, _ID))
                self.logger.debug('dio Thread created. pid=' + str(pid_int))

                t.start()                
                self.logger.debug('dio Thread started. pid=' + str(pid_int))

            except Exception as ex:
                self.logger.info("Error: " + repr(ex))
                #errormessage = "Error"
                self.logger.info('Error HHTP not expected: ' + repr(ex))
            #

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++DioSendVProfileData Error: ' + repr(ex)

        self.logger.info('***Method->-DIO sendVProfileData ENDS')
        return errormessage
    #fin sendData



    """
    * Envia peticion de borrado de los datos de una session en google datastore
    *
    * @param _idSesion Identificador de la sesion a eliminar
    """
    def deleteSession(self, _idSesion):

        self.logger.debug('***Method->-DIO DeleteSession INIT')

        errormessage = '0'
        result = 0

        try:
            url = Constantes.WEB_URL_DELETE_SESSION_IBEX_HOST + str(_idSesion)

            self.logger.info('Deleting Session=' + str(url))

            resp = requests.delete(url,
                                headers={'Content-Type':'application/json'},
                                auth=(ConfigRoot.user, ConfigRoot.pasw))

            status_result = resp.status_code
            if 200 == resp.status_code:
                self.logger.debug('response status=' + resp.json()['status'])
                self.logger.debug('response operation=' + resp.json()['operation'])
                self.logger.debug('response deleted=' + resp.json()['deleted'])

                result = resp.json()['deleted']
            #
            else:
                # This means something went wrong.
                self.logger.debug("Error calling api-rest: " + str(resp.status_code))
                errormessage = "Error DIO. status-code="  + str(resp.status_code) + ', status=' + str(resp.json()['status'])
            #

        except Exception as ex:
            self.logger.error(repr(ex.args))
            self.logger.exception(ex)
            errormessage = '++--++Dio DeleteSession Error: ' + repr(ex)

        self.logger.info('***Method->-DIO DeleteSession ENDS (' + str(result) + ')')
        return errormessage
    #fin deleteSession
#class
