#!/usr/bin/env python
""" Threading worker for api rest requests

    @author Alfredo Sanz
    @date July 2017
"""

#APIs imports
import logging
import logging.config
import time
from decimal import *
import requests   #for normal 
import simplejson as json

#local imports
from model.Singleton_DataTemp import Singleton_DataTemp
from common import Util
from common import Constantes
import ConfigRoot

def send_data_ibex35(_logger, _thedata, _pid_int, _ID):

    _logger.info('***Method->-WORKER DIO send_data_ibex35 INIT. pid:' + str(_pid_int) +', ID=' + str(_ID))

    try:
        resp = requests.post(Constantes.WEB_URL_DATA_IBEX_HOST,
                            json=_thedata,  #json.dumps(_thedata, separators=(',', ':'), sort_keys=True),
                            headers={'Content-Type':'application/json'},
                            auth=(ConfigRoot.user, ConfigRoot.pasw))
        _logger.debug('Request post ends. pid:' + str(_pid_int))

    except Exception as ex:
        _logger.info("Error: " + repr(ex))
        _logger.info('Error HHTP not expected: ' + repr(ex) + '. pid:' + str(_pid_int))
    #

    _logger.info('***Method->-WORKER DIO send_data_ibex35 ENDS. pid:' + str(_pid_int))
#fin send_data_ibex35



def send_vprofiledata_ibex35(_logger, _thedata, _pid_int, _ID):

    _logger.info('***Method->-WORKER DIO send_data_ibex35 INIT. pid:' + str(_pid_int) +', ID=' + str(_ID))

    try:
        resp = requests.post(Constantes.WEB_URL_DATA_VPROFILE_HOST,
                            json=_thedata,  #json.dumps(_thedata, separators=(',', ':'), sort_keys=True),
                            headers={'Content-Type':'application/json'},
                            auth=(ConfigRoot.user, ConfigRoot.pasw))
        _logger.debug('Request post ends. pid:' + str(_pid_int))

    except Exception as ex:
        _logger.info("Error: " + repr(ex))
        _logger.info('Error HHTP not expected: ' + repr(ex) + '. pid:' + str(_pid_int))
    #

    _logger.info('***Method->-WORKER DIO send_vprofiledata_ibex35 ENDS. pid:' + str(_pid_int))
#fin send_vprofiledata_ibex35
