#!/usr/bin/env python
""" Common File
    Utility functions
    
    @author Alfredo Sanz
    @date Febrero 2017
"""
#APIs imports
import os
from datetime import date, timedelta, datetime
import time
import pytz
import string
import math

#local Imports
from common import Constantes


def datetimeFechaToStringFecha(_dtdtFecha):

    result = _dtdtFecha.strftime("%d/%m/%Y")

    return result
#fin datetimeFechaToStringFecha



#Genera un numero entero basado en la fecha y hora
def generateDateTimeBasedKey():

    #current_time = time.time()
    #result = int(current_time) + os.getpid()

    madrid = pytz.timezone("Europe/Madrid")
    dtdt = datetime.now(madrid)
    dt = dtdt.date()
    tm = dtdt.time()

    mdate = dtdt.date()
    mtime = dtdt.time()

    milisec = str(int(dtdt.microsecond / 1000))
    while 3 > len(milisec):
        milisec = '0' + milisec
    #

    result = int(mdate.strftime("%d%m%Y") + mtime.strftime("%H%M%S") + milisec)

    return result
#fin generateDateTimeBasedKey



"""
* Obtiene el timestamp de la fecha/hora actuales
* devolviendo la parte entera. Precision = segundos.
*
* @return int con el timestamp acutal en segundos
"""
def getCurrentTimeInSeconds():

    dtdt = datetime.utcnow()
    ts = dtdt.timestamp()
    result = int(ts)

    return result
#fin getCurrentTimeInSeconds



def getMonthstrByMonthnumber(_intMonth):

    result = ''

    if 1 == _intMonth:
        result = u'Enero'
    elif 2 == _intMonth:
        result = u'Febrero'
    elif 3 == _intMonth:
        result = u'Marzo'
    elif 4 == _intMonth:
        result = u'Abril'
    elif 5 == _intMonth:
        result = u'Mayo'
    elif 6 == _intMonth:
        result = u'Junio'
    elif 7 == _intMonth:
        result = u'Julio'
    elif 8 == _intMonth:
        result = u'Agosto'
    elif 9 == _intMonth:
        result = u'Septiembre'
    elif 10 == _intMonth:
        result = u'Octubre'
    elif 11 == _intMonth:
        result = u'Noviembre'
    elif 12 == _intMonth:
        result = u'Diciembre'
    #

    return result
#fin getMonthstrByMonthnumber



"""
* Reemplaza en Mes en Ingles por el Mes en Espanol
* de la cadena del parametro y segun el 
"""
def __replaceMonth(_strFecha, _intMonth):

    result = ''

    if 1 == _intMonth:
        result = _strFecha.replace('January', u'Enero')
    elif 2 == _intMonth:
        result = _strFecha.replace('February', u'Febrero')
    elif 3 == _intMonth:
        result = _strFecha.replace('March', u'Marzo')
    elif 4 == _intMonth:
        result = _strFecha.replace('April', u'Abril')
    elif 5 == _intMonth:
        result = _strFecha.replace('May', u'Mayo')
    elif 6 == _intMonth:
        result = _strFecha.replace('June', u'Junio')
    elif 7 == _intMonth:
        result = _strFecha.replace('July', u'Julio')
    elif 8 == _intMonth:
        result = _strFecha.replace('August', u'Agosto')
    elif 9 == _intMonth:
        result = _strFecha.replace('September', u'Septiembre')
    elif 10 == _intMonth:
        result = _strFecha.replace('October', u'Octubre')
    elif 11 == _intMonth:
        result = _strFecha.replace('November', u'Noviembre')
    elif 12 == _intMonth:
        result = _strFecha.replace('December', u'Diciembre')
    #

    return result
#__replaceMonth




"""
* Obtiene la hora actual y la devuelve en disgregada en
* tres valores diferentes:  fecha, hora, y fecha/hora en
* formato largo, pero el mes en formato String en Espanol
* y no como numero.
*
* @return dict{dtdt, intDate, intTime, strFechaHora, strFechaHoraFilename, strFechaHoraFilenameST, strFecha, intYear, intMonth, intDay, intHour, intMin, intSec}
"""
def getCurrentTime_months(_logger):

    result = {}

    result_date = 0
    result_time = 0
    result_sesion_format = '0'
    result_fecha_str = '0'

    madrid = pytz.timezone("Europe/Madrid")
    dtdt = datetime.now(madrid)
    dt = dtdt.date()
    tm = dtdt.time()

    result_ts = int(dtdt.timestamp())

    mdate = dtdt.date()
    result_date = int(mdate.strftime("%Y%m%d"))
    result_year = int(mdate.strftime("%Y"))  #breakdown year
    result_month = int(mdate.strftime("%m")) #breakdown month
    result_day = int(mdate.strftime("%d"))   #breakdown day

    mtime = dtdt.time()
    result_time = int(mtime.strftime("%H%M%S"))
    result_hour = int(mtime.strftime("%H"))     #breakdown hour
    result_min = int(mtime.strftime("%M"))      #breakdown minute
    result_sec = int(mtime.strftime("%S"))      #breakdown second

    result_sesion_format = mdate.strftime(u"%d-%B-%Y") + " " + mtime.strftime(u"%H:%M:%S")
    result_sesion_format = result_sesion_format.encode('utf-8').decode('utf-8')
    result_sesion_format = __replaceMonth(result_sesion_format, mdate.month)

    result_milisec = int(dtdt.microsecond / 1000)
    milisec = str(result_milisec)
    while 3 > len(milisec):
        milisec = '0' + milisec
    #
    result_sesion_format_mili = mdate.strftime(u"%d-%B-%Y") + " " + mtime.strftime(u"%H:%M:%S") + ':' + milisec
    result_sesion_format_mili = result_sesion_format_mili.encode('utf-8').decode('utf-8')
    result_sesion_format_mili = __replaceMonth(result_sesion_format_mili, mdate.month)

    result_fechahora_filename = mdate.strftime(u"%d_%m_%Y") + "__" + mtime.strftime(u"%H_%M_%S")
    result_fechahora_filename = result_fechahora_filename.encode('utf-8').decode('utf-8')

    result_fechahora_filename_st = mdate.strftime(u"%d_%m_%Y") + "-" + mtime.strftime(u"%H_%M_%S")
    result_fechahora_filename_st = result_fechahora_filename_st.encode('utf-8').decode('utf-8')

    result_fecha_str = mdate.strftime(u"%d-%B-%Y")
    result_fecha_str = result_fecha_str.encode('utf-8').decode('utf-8')
    result_fecha_str = __replaceMonth(result_fecha_str, mdate.month)

    result['dtdt'] = dtdt
    result['result_ts'] = result_ts
    result['intDate'] = result_date
    result['intTime'] = result_time
    result['strFechaHora'] = result_sesion_format
    result['strFechaHora_mil'] = result_sesion_format_mili
    result['strFechaHoraFilename'] = result_fechahora_filename
    result['strFechaHoraFilenameST'] = result_fechahora_filename_st
    result['strFecha'] = result_fecha_str
    result['year'] = result_year
    result['month'] = result_month      #int
    result['day'] = result_day          #int
    result['hour'] = result_hour        #int
    result['minute'] = result_min       #int
    result['second'] = result_sec       #int
    result['milisec'] = result_milisec  #int

    _logger.debug('getCurrentTime_months: ' + repr(result))
    return result
#fin getCurrentTime_months



"""
* Obtiene la hora actual y la devuelve en disgregada en
* tres valores diferentes:  fecha, hora, y fecha/hora en
* formato largo.
*
* @return dict{dtdt, intDate, intTime, strFechaHora, strFechaHoraFilename, strFechaHoraFilenameST, strFecha, intYear, intMonth, intDay, intHour, intMin, intSec}
"""
def getCurrentTime(_logger):

    result = {}

    result_date = 0
    result_time = 0
    result_sesion_format = '0'
    result_fecha_str = '0'
    result_ts = 0

    madrid = pytz.timezone("Europe/Madrid")
    dtdt = datetime.now(madrid)
    dt = dtdt.date()
    tm = dtdt.time()

    result_ts = int(dtdt.timestamp())

    mdate = dtdt.date()
    result_date = int(mdate.strftime("%Y%m%d"))
    result_year = int(mdate.strftime("%Y"))  #breakdown year
    result_month = int(mdate.strftime("%m")) #breakdown month
    result_day = int(mdate.strftime("%d"))   #breakdown day

    mtime = dtdt.time()
    result_time = int(mtime.strftime("%H%M%S"))
    result_hour = int(mtime.strftime("%H"))     #breakdown hour
    result_min = int(mtime.strftime("%M"))      #breakdown minute
    result_sec = int(mtime.strftime("%S"))      #breakdown second

    result_milisec = int(dtdt.microsecond / 1000)
    milisec = str(result_milisec)
    while 3 > len(milisec):
        milisec = '0' + milisec
    #
    result_sesion_format_mili = mdate.strftime(u"%d-%B-%Y") + " " + mtime.strftime(u"%H:%M:%S") + ':' + milisec
    result_sesion_format_mili = result_sesion_format_mili.encode('utf-8').decode('utf-8')
    result_sesion_format_mili = __replaceMonth(result_sesion_format_mili, mdate.month)

    result_sesion_format = mdate.strftime(u"%d-%m-%Y") + " " + mtime.strftime(u"%H:%M:%S")
    result_sesion_format = result_sesion_format.encode('utf-8').decode('utf-8')

    result_fecha_str = mdate.strftime(u"%d-%B-%Y")
    result_fecha_str = result_fecha_str.encode('utf-8').decode('utf-8')

    result_fechahora_filename = mdate.strftime(u"%d/%m/%Y") + " - " + mtime.strftime(u"%H:%M:%S")
    result_fechahora_filename = result_fechahora_filename.encode('utf-8').decode('utf-8')

    result_fechahora_filename_st = mdate.strftime(u"%d_%m_%Y") + "-" + mtime.strftime(u"%H_%M_%S")
    result_fechahora_filename_st = result_fechahora_filename_st.encode('utf-8').decode('utf-8')

    result['dtdt'] = dtdt
    result['result_ts'] = result_ts
    result['intDate'] = result_date
    result['intTime'] = result_time
    result['strFechaHora'] = result_sesion_format
    result['strFechaHora_mil'] = result_sesion_format_mili
    result['strFechaHoraFilename'] = result_fechahora_filename
    result['strFechaHoraFilenameST'] = result_fechahora_filename_st
    result['strFecha'] = result_fecha_str
    result['year'] = result_year
    result['month'] = result_month
    result['day'] = result_day
    result['hour'] = result_hour
    result['minute'] = result_min
    result['second'] = result_sec
    result['milisec'] = result_milisec  #int

    _logger.debug('getCurrentTime: ' + repr(result))
    return result
#fin getCurrentTime



"""
* Obtiene la Hora actual menos un periodo de tiempo.
*
* @param _dtdt Datetime con la fecha hora actual
* @param _period Indica la cantidad de Minutos a Restar.
*       valores posibles: 1H, 2M
*
* @result int con la hora menos el periodo.
"""
def getCurrentHourTimeMinusMinutes(_dtdt, _period):

    result = None
    new_dt = None

    if '1H' == _period:
        new_dt = _dtdt - timedelta(minutes=60)
    elif '2M' == _period:
        new_dt = _dtdt - timedelta(minutes=2)
    else:
        new_dt = _dtdt - timedelta(minutes=0)
    #

    mtime = new_dt.time()
    result = int(mtime.strftime("%H%M%S"))

    return result
#fin getCurrentHourTimeMinusMinutes



"""
* Calcula una diferencia de tiempo entre dos timestamps (segundos, sin la parte real),
* y el resultado puede ser en segundos o en Minutos,
* dependiendo del parametro unit.
* El resultado en minutos es con precision de minutos, es decir, 1 minuto, 2 minutos, etc...
*
* @param curTime  timestamp en segundos sin parte real
* @param lastTime   timestamp en segundos sin parte real
* @param unit S,M -> indica si se quiere el resultado en minutos o segundos.
*
* @return int         ->El numero de unidades de diferencia de tiempo, 
*                       en segundos o minutos
*                       En el caso de los minutos, solo devuelve unidades enteras
*                       con redondeo a la baja. Por ejemplo: 30 segundos serian 0 minutos.
*                                                            75 segundos serian 1 minuto.
*                     -> 0 en caso de error durante el calculo
"""
def diffTimes(curTime, lastTime, unit, _logger):

    result = 0
    _logger.debug('initT=' + str(curTime) + ', endTime=' + str(lastTime))
    try:
        if Constantes.TIME_UNIT_SEC == unit:
            result = curTime - lastTime
        elif Constantes.TIME_UNIT_MIN == unit:
            diff_secs = curTime - lastTime
            diff_mins_float = diff_secs / 60
            result = int(diff_mins_float)  #Nos quedamos con la parte entera, down round.
        #
        else:
            result = 0
        #

    except Exception as ex:
        _logger.error("Error Calculating diff time: ", ex)
        result = 0

    _logger.debug('diff=' + str(result))
    return result
#fin diffTimes



def diffTimesMilliseconds(curTime_dtdt, lastTime_dtdt, _logger):

    result = 0
    _logger.debug('initT=' + repr(curTime_dtdt) + ', endTime=' + repr(lastTime_dtdt))

    try:
        diff_tmdelta = curTime_dtdt - lastTime_dtdt
        _logger.debug('diff_tmdelta=' + repr(diff_tmdelta))

        miliseconds_01 = diff_tmdelta.seconds * 1000
        miliseconds_02 = diff_tmdelta.microseconds / 1000
        result = miliseconds_01 + miliseconds_02
        result = int(result) #-> cogemos la parte entera

    except Exception as ex:
        _logger.error('Error Calculating diff time miliseconds ', ex)
        result = 0

    _logger.debug('diff_microse=' + str(result))
    return result
#fin diffTimesMilliseconds



def generate_timeobj(_year, _month, _day, _hour, _minute, _second, _logger):

    result = {}

    result_date = 0
    result_time = 0
    result_sesion_format = '0'
    result_fecha_str = '0'

    madrid = pytz.timezone("Europe/Madrid")
    dtdt_i = datetime.now(madrid)
    
    iyear = int(_year)
    imonth = int(_month)
    iday = int(_day)
    ihour = int(_hour)
    iminute = int(_minute)
    isecond = int(_second)
    #replace([year[, month[, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]]]]])
    dtdt = dtdt_i.replace(year=iyear, month=imonth, day=iday, hour=ihour, minute=iminute, second=isecond)

    mdate = dtdt.date()
    result_date = int(mdate.strftime("%Y%m%d"))
    result_year = int(mdate.strftime("%Y"))  #breakdown year
    result_month = int(mdate.strftime("%m")) #breakdown month
    result_day = int(mdate.strftime("%d"))   #breakdown day

    mtime = dtdt.time()
    result_time = int(mtime.strftime("%H%M%S"))
    result_hour = int(mtime.strftime("%H"))     #breakdown hour
    result_min = int(mtime.strftime("%M"))      #breakdown minute
    result_sec = int(mtime.strftime("%S"))      #breakdown second

    result_sesion_format = mdate.strftime(u"%d-%m-%Y") + " " + mtime.strftime(u"%H:%M:%S")
    result_sesion_format = result_sesion_format.encode('utf-8').decode('utf-8')

    result_fecha_str = mdate.strftime(u"%d-%B-%Y")
    result_fecha_str = result_fecha_str.encode('utf-8').decode('utf-8')

    result_fechahora_filename = mdate.strftime(u"%d/%m/%Y") + " - " + mtime.strftime(u"%H:%M:%S")
    result_fechahora_filename = result_fechahora_filename.encode('utf-8').decode('utf-8')

    result_fechahora_filename_st = mdate.strftime(u"%d_%m_%Y") + "-" + mtime.strftime(u"%H_%M_%S")
    result_fechahora_filename_st = result_fechahora_filename_st.encode('utf-8').decode('utf-8')

    result['dtdt'] = dtdt
    result['intDate'] = result_date
    result['intTime'] = result_time
    result['strFechaHora'] = result_sesion_format
    result['strFechaHoraFilename'] = result_fechahora_filename
    result['strFechaHoraFilenameST'] = result_fechahora_filename_st
    result['strFecha'] = result_fecha_str
    result['year'] = result_year
    result['month'] = result_month
    result['day'] = result_day
    result['hour'] = result_hour
    result['minute'] = result_min
    result['second'] = result_sec

    return result
#fin generate_timeobj



def getHourOfDay():

    madrid = pytz.timezone("Europe/Madrid")
    dtdt = datetime.now(madrid)

    result = dtdt.hour
    return result
#fin getHourOfDay



def thousandsDots(_mystring):

    result_1 = "{0:,}".format(int(_mystring))
    result = result_1.replace(',', '.')

    return result
#fin thousandsDots



def thousandsDotsInt(_myInt):

    result_1 = "{0:,}".format(_myInt)
    result = result_1.replace(',', '.')

    return result
#fin thousandsDots



def getListOfYears():
    """
    * Devuelve una lista de anos<int> en el rango configurado
    * por las contantes.
    """

    result = []

    year = Config.YEARS_LIST_START_AT
    i = 0
    while True:
        result.append(year)

        if i >= Config.YEARS_LIST_MAX_NUMBER:
            break
        #

        i += 1
        year += 1
    #

    return result
#fin getListOfYears



def formatDateTimeIntCompleteZeros(_year, _month, _day, _hour):

    result = ''

    str_year = str(_year)
    result += str_year

    str_month = str(_month)
    if 10 > int(_month):
        str_month = '0' + str(_month)
    #
    result += str_month

    str_day = str(_day)
    if 10 > int(_day):
        str_day = '0' + str(_day)
    #
    result += str_day

    str_hour = str(_hour)
    if 10 > int(_hour):
        str_hour = '0' + str(_hour)
    #
    result += str_hour

    return result.encode('utf-8').decode('utf-8')
#fin formatDateTimeIntCompleteZeros



def compareDatetimes_hours(_datetime_A, _datetime_B, logging):
    """return hours<int>, minutes<int>, seconds<int>"""

    diff_timedelta = _datetime_B - _datetime_A #d.days, d.seconds, d.microseconds

    logging.info('**diff_timedelta:' + repr(diff_timedelta))
    logging.info('**diff_timedelta.seconds:' + repr(diff_timedelta.days) + 
                        ' days, ' + repr(diff_timedelta.seconds) + 
                        ' seconds, ' + repr(diff_timedelta.microseconds) + 
                        ' microseconds')

    result_hour = diff_timedelta.seconds // 3600
    logging.info('**result_hour:' + str(result_hour))

    result_min = (diff_timedelta.seconds // 60) % 60
    logging.info('****result_min: ' + str(result_min))

    result_sec = diff_timedelta.seconds % 60
    logging.info('****result_sec: ' + str(result_sec))

    #ajuste diario
    if diff_timedelta.days:
        dd = 24 * diff_timedelta.days
        result_hour += dd
    #
    logging.info('****diff_total, result_hour: ' + str(result_hour) + 
                                ' result_min: ' + str(result_min) + 
                                ' result_sec: ' + str(result_sec))

    return result_hour, result_min, result_sec
#fin compareDatetimes_hours



def getListdaysOfMonth(_inputYear, _inputMonth, _logger):
    """ return result_day_number ['01', '02', ..], result_day_name['lunes', ....]"""

    result_day_number = []
    result_day_name = []

    # @see https://stackoverflow.com/questions/9847213/which-day-of-week-given-a-date-python
    day_list = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

    theday = 1
    while True:
        if 31 < theday:
            _logger.info('*****theday break')
            break
        #

        try:
            dayweek_int = date(_inputYear, _inputMonth, theday).weekday()
            midia_name = day_list[dayweek_int]

        except Exception as ex:
            _logger.debug('*****Exception: ' + repr(ex))
            break
        #

        result_day_number.append(str(theday))
        result_day_name.append(midia_name)

        theday += 1
    #while

    return result_day_number, result_day_name
#fin getListdaysOfMonth



"""
    * key = str<year-month-day>
    * ex:'2017-07-01'
"""
def getCurrentCalendarKey():

    madrid = pytz.timezone("Europe/Madrid")
    dtdt = datetime.now(madrid)
    dt = dtdt.date()
    tm = dtdt.time()

    mdate = dtdt.date()
    result = mdate.strftime("%Y-%m-%d")

    return result
#fin getCurrentCalendarKey