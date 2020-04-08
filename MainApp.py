#!/usr/bin/env python
""" Aplicacion principal del Trading de Alfredo
    para gestionar los datos que se van a enviar
    a GAE para la web

    @author Alfredo Sanz
    @date Marzo 2019
    @version 2
"""

#APIs imports
import cmd, sys, os
import logging
import logging.config
from common import Constantes

#local imports
from ETDA_Ibex_Engine import ETDA_ibex_Engine
from ETDA_Dec_Engine import ETDA_Dec_Engine
from StopProcessCondition import StopProcessConditionSingleton



class MainApp(cmd.Cmd):

    intro = '\nWelcome to Eltradingdealf-Realtime-Data-Sender Application. Type ? for commands\n Ctrl-C para parar la ejecucion del proceso.'
    prompt = 'ETDA: type action-> '
    spc = StopProcessConditionSingleton()


    """
    * Constructor
    *
    * Carga el controlador de la consola y el manejador de Logging
    """
    def __init__(self):
        cmd.Cmd.__init__(self)

        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('PYDACALC2')

        self.ibexDataProcess = ETDA_ibex_Engine()
        self.decimal_DataProcess = ETDA_Dec_Engine()
    #construct



    """
    * Start reading and sending data.
    """
    def do_init(self, arg):
        'Starts Process reading and sending data'  #Comment for commands help

        self.logger.info('Main.do_start->Starting proccess')

        self.spc.stopProcessFlag = False
        self.ibexDataProcess.dowork()
    #do_start



    """
    * Start reading and sending data for Euro-FX.
    """
    def do_init_euroFX(self, arg):
        'Starts Process reading and sending data for Euro-FX'  #Comment for commands help

        self.logger.info('Main.do_start->Starting proccess')

        self.spc.stopProcessFlag = False
        market = Constantes.MARKET_EUROFX

        self.decimal_DataProcess.dowork(market)
    #do_start



    """
    * Exit App
    """
    def do_quit(self, arg):
        'Exit application'
        self.logger.info('Application closing. Have a nice day!.')
        #sys.exit(0)
        #os._exit(1)
        quit()
    #do_quit



    def cmdloop_with_keyboard_interrupt(self):
        doQuit = False
        while doQuit != True:
            try:
                self.cmdloop()
                doQuit = True
            except KeyboardInterrupt:
                sys.stdout.write('\n')
            finally:
                self.logger.info('Stopping proccess: Flag==%s', str(self.spc.stopProcessFlag))
                self.spc.stopProcessFlag = True
                self.logger.info('Stopping proccess: Flag==%s', str(self.spc.stopProcessFlag))
        #while
    #cmdloop_with_keyboard_interrupt
#fin class


#----MAIN EXECUTION----


app = MainApp()
#app.cmdloop()
app.cmdloop_with_keyboard_interrupt()
