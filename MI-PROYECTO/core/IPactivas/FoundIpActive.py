#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################
# se determina si las IPs de un rango dado estan     #
# activas, es decir levantadas o no, las IP activas  #
# se indicn en pantalla, se valida IP y rango de     #
# las mismas.                                        #
######################################################

######################################################
# import de librerias                                #
######################################################
import os
import subprocess
import sys
from termcolor import colored
import ipaddress
######################################################
# clase para ping a IPs                              #
######################################################
class encontrarIps():
    def __init__(self,IP,rangoDesde,rangoHasta):
        self.IP=IP
        self.rangoDesde=rangoDesde
        self.rangoHasta=rangoHasta

    def validarRangoD(self,rangoDesde):
        if  len(rangoDesde)==0 or rangoDesde.isdigit()==False:
            print(colored('[-] Rango desde para IP no numerico o no informado','red',attrs=['bold']))
            exit()

    def validarRangoH(self,rangoHasta):
        if  len(rangoHasta)==0 or rangoHasta.isdigit()==False:
            print(colored('[-] Rango hasta para IP no numerico o no informado','red',attrs=['bold']))
            exit()

    def comparaRangos(self,rangoDesde,rangoHasta):
        if rangoDesde > rangoHasta:
            print(colored('[-] Rango desde no puede ser mayor que hasta','red',attrs=['bold']))
            exit()

    def validaIp(self,IP):
        try:
            ipaddress.ip_address(IP)
            return True
        except:
            return False

####################################################
# Se borra las pantalla
####################################################
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")
####################################################
# Menu principal,se pide tres octetos de la IP y
# se pide el rango desde y rango hasta,se validar
# si los rangos introducidos son numericos y si el
# rango desde es menos que rango hasta.Se valida
# IP creada con los rangos y si es correcta se hace
# ping a la IP si esta responde, se envia print a
# la salida, solo las IPs que estan activas.
###################################################
def IPactiv():
    borrarPantalla()
    print(colored('*************************************************','green',attrs=['bold']))
    print(colored('        IPs ACTIVAS EN LA RED                    ','green',attrs=['bold']))
    print(colored('*************************************************','green',attrs=['bold']))

    octeto=input(colored('Introduzaca los tres primeros octetos de la IP XXX.XXX.XXX: ','green',attrs=['bold']))
    rangoD=input(colored('Introduzaca rango desde del ultimo octeto de la IP: ','green',attrs=['bold']))
    rangoH=input(colored('Introduzaca rango haste del ultimo octeto de la IP: ','green',attrs=['bold']))
    print('                                                                                                     ')

    valido=encontrarIps(octeto,rangoD,rangoH)
    valido.validarRangoD(rangoD)
    valido.validarRangoH(rangoH)
    valido.comparaRangos(rangoD,rangoH)

    rdesde=int(rangoD)
    rhasta=int(rangoH)

    for cuartoOcteto in range(rdesde,(rhasta+1)):
        ipvictima=octeto + '.' + str(cuartoOcteto)

        IpOK=valido.validaIp(ipvictima)

        if IpOK:
            print(colored('IP a escanear: ','green',attrs=['bold']),colored(ipvictima,'cyan',attrs=['bold']))#IpUP=os.system("ping -c 1 " + ipvictima)
            IpUP=subprocess.Popen(["ping", "-c 1", ipvictima], stdout=subprocess.PIPE)
            datosIp = IpUP.communicate()[0]

            if not 'Destination Host Unreachable' in str(datosIp):
                print(colored('***********************************************************************','green',attrs=['bold']))
                print(colored('[+] La IP: ','green',attrs=['bold']),colored(ipvictima,'cyan',attrs=['bold']),colored(' esta levantada','green',attrs=['bold']))
                print(colored('***********************************************************************','green',attrs=['bold']))
                print('                                                                                                       ')
        else:
            print(colored('[-] Ip introducida ' + ipvictima + ' no valida','red',attrs=['bold']))
            exit()
