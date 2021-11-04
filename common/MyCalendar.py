#!/usr/bin/env python
""" Common File
    Dict con el calendario de sesiones
    
    @author Alfredo Sanz
    @date Julio 2017
    @update 20Marzo2018
"""
#APIs imports


"""key str<year-month-day>, value [openmarket str<Y/N/F>, 
                                   openmarket hour  int<h>, 
                                   closemarket hour int<h>],
                                   backup_done int<0/1>"""
thecalendar_ibex35 = {
                        '2021-09-01':['S', 8, 22, 0],
                        '2021-09-02':['S', 8, 22, 0],
                        '2021-09-03':['S', 8, 22, 0],
                        '2021-09-04':['S', 8, 22, 0],
                        '2021-09-05':['N', 0, 0, 0],#SABADO
                        '2021-09-06':['N', 0, 0, 0],
                        '2021-09-07':['S', 8, 22, 0],
			            '2021-09-08':['S', 8, 22, 0],
                        '2021-09-09':['S', 8, 22, 0],
			            '2021-09-10':['S', 8, 22, 0],
                        '2021-09-11':['S', 8, 22, 0],
                        '2021-09-12':['N', 0, 0, 0],#SABADO
                        '2021-09-13':['N', 0, 0, 0],
                        '2021-09-14':['S', 8, 22, 0],
			            '2021-09-15':['S', 8, 22, 0],
                        '2021-09-16':['S', 8, 22, 0],
			            '2021-09-17':['S', 8, 22, 0],
                        '2021-09-18':['S', 8, 22, 0],
                        '2021-09-19':['N', 0, 0, 0],#SABADO
                        '2021-09-20':['N', 0, 0, 0],
                        '2021-09-21':['S', 8, 24, 0],
			            '2021-09-22':['S', 8, 22, 0],
                        '2021-09-23':['S', 8, 24, 0],
			            '2021-09-24':['S', 8, 22, 0],
                        '2021-09-25':['S', 8, 22, 0],
			            '2021-09-26':['N', 0, 0, 0],#SABADO
			            '2021-09-27':['N', 0, 0, 0],
                        '2021-09-28':['S', 8, 24, 0],
			            '2021-09-29':['S', 8, 24, 0],
                        '2021-09-30':['S', 8, 22, 0],
                        '2021-10-01':['S', 8, 22, 0]
}



"""key str<year-month-day>, value [openmarket str<Y/N/F>, 
                                   openmarket hour  int<h>, 
                                   closemarket hour int<h>],
                                   backup_done int<0/1>"""
thecalendar_FuturesCME = {                        
                        '2021-11-01':['S', 8, 22, 0],
                        '2021-11-02':['S', 8, 22, 0],
                        '2021-11-03':['S', 8, 22, 0],
                        '2021-11-04':['S', 8, 22, 0],
                        '2021-11-05':['S', 8, 22, 0],
                        '2021-11-06':['N', 0, 0, 0],#SABADO
                        '2021-11-07':['N', 0, 0, 0],#SABADO
			            '2021-11-08':['S', 8, 22, 0],
                        '2021-11-09':['S', 8, 22, 0],
			            '2021-11-10':['S', 8, 22, 0],
                        '2021-11-11':['S', 8, 22, 0],
                        '2021-11-12':['S', 8, 22, 0],
                        '2021-11-13':['N', 0, 0, 0],#SABADO
                        '2021-11-14':['N', 0, 0, 0],#SABADO
			            '2021-11-15':['S', 8, 22, 0],
                        '2021-11-16':['S', 8, 22, 0],
			            '2021-11-17':['S', 8, 22, 0],
                        '2021-11-18':['S', 8, 22, 0],
                        '2021-11-19':['S', 8, 22, 0],
                        '2021-11-20':['N', 0, 0, 0],#SABADO
                        '2021-11-21':['N', 0, 0, 0],#SABADO
			            '2021-11-22':['S', 8, 22, 0],
                        '2021-11-23':['S', 8, 22, 0],
			            '2021-11-24':['S', 8, 22, 0],
                        '2021-11-25':['S', 8, 22, 0],
			            '2021-11-26':['S', 8, 22, 0],
			            '2021-11-27':['N', 0, 0, 0],#SABADO
                        '2021-11-28':['N', 0, 0, 0],#SABADO
			            '2021-11-29':['S', 8, 22, 0],
                        '2021-11-30':['S', 8, 22, 0],
                        '2021-12-01':['S', 8, 22, 0],
                        '2021-12-02':['S', 8, 22, 0],
                        '2021-12-03':['S', 8, 22, 0],
                        '2021-12-04':['N', 0, 0, 0],#SABADO
                        '2021-12-05':['N', 0, 0, 0],#SABADO
			            '2021-12-06':['S', 8, 22, 0],
                        '2021-12-07':['S', 8, 22, 0],
			            '2021-12-08':['S', 8, 22, 0],
                        '2021-12-09':['S', 8, 22, 0],
                        '2021-12-10':['S', 8, 22, 0],
                        '2021-12-11':['N', 0, 0, 0],#SABADO
                        '2021-12-12':['N', 0, 0, 0],#SABADO
			            '2021-12-13':['S', 8, 22, 0],
                        '2021-12-14':['S', 8, 22, 0],
			            '2021-12-15':['S', 8, 22, 0],
                        '2021-12-16':['S', 8, 22, 0],
                        '2021-12-17':['S', 8, 22, 0],
                        '2021-12-18':['N', 0, 0, 0],#SABADO
                        '2021-12-19':['N', 0, 0, 0],#SABADO
			            '2021-12-20':['S', 8, 22, 0],
                        '2021-12-21':['S', 8, 22, 0],
			            '2021-12-22':['S', 8, 22, 0],
                        '2021-12-23':['S', 8, 22, 0],
			            '2021-12-24':['S', 8, 22, 0],
			            '2021-12-25':['N', 0, 0, 0],#SABADO
                        '2021-12-26':['N', 0, 0, 0],#SABADO
			            '2021-12-27':['S', 8, 22, 0],
                        '2021-12-28':['S', 8, 22, 0],
                        '2021-12-29':['S', 8, 24, 0],
                        '2021-12-30':['S', 8, 24, 0],
                        '2021-12-31':['S', 8, 24, 0],
}