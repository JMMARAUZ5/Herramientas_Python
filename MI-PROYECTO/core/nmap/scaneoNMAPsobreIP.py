#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################################################################
#                           scaneoNMAPsobreIP                                    #
#  Se realizara un scaneo sobre una IP                                           #
#  asi como sobre un puerto ,intervalo de puertos predeterminado                 #
#  o todos los puertos                                                           #
#  este modulo se invoca para una IP o para un rango de IPs                      #
##################################################################################

##################################################################################
# import a realizar                                                              #
##################################################################################
import nmap
import sys
import os
import time
from termcolor import colored
######################################################
# Se decide que modalidad de scaneo de puertos se    #
# elijara                                            #
# 1.-scaneo todos los puertos                        #
# 2.-scaneo puertos predeterminados                  #
# 3.-scaneo de un solo puerto                        #
######################################################
def elegirOpcionPuertos():

    print(colored("1.-SCANEO DE TODOS LOS PUERTOS",'green',attrs=['bold']))
    print(colored("2.-SCANEO PUERTOS PREDETERMINADOS",'green',attrs=['bold']))
    print(colored("3.-SCANEO DE UN SOLO PUERTO",'green',attrs=['bold']))
    print(colored("                                      ",'green',attrs=['bold']))

    opcion=input(colored("POR FAVOR,ELEGIR OPCION: ",'green',attrs=['bold']))

    if opcion == "1" or opcion =="2" or opcion =="3":
        return opcion
    else:
        print(colored("[-] OPCION ERRONEA AL ELEGIR MODALIDAD SCANEO DE PUERTOS",'red',attrs=['bold']))
        print(colored("                                      ",'green',attrs=['bold']))
        time.sleep(2)
        exit()

######################################################
# Se realiza el scaneo sobre una IP                  #
# se valida que existe la ip y si existe que esta    #
# este levantada.                                    #
######################################################
def MiscaneoNMAPsobreIP(IPEntrada):

    scaneoIP=nmap.PortScanner()
    scaneoIP.scan(IPEntrada)
    print('                                                                                 ')
    print(colored('Este proceso puede llevar unos minutos,paciencia por favor....','green',attrs=['bold']))
    print('                                                                               ')

    try:
        if not scaneoIP.all_hosts():
            print (colored("NO HAY HOST,LA IP NO EXISTE O NO SE PUEDE ACCEDER A ELLA",'red',attrs=['bold']))
            print("                                                       ")
            time.sleep(2)

        else:

            hostStatus=scaneoIP[IPEntrada].state()

            if hostStatus=="up":

                resultOPcionPuertos=elegirOpcionPuertos()

                if resultOPcionPuertos=="1":

                    print(colored("Al generar gran cantidad de informacion,esta se envia a fichero",'green',attrs=['bold']))
                    print(colored("Se encontrara en la ruta: ",'green',attrs=['bold']))

                    name_dirSalida = os.path.join(os.path.dirname(__file__),'FICH_SAL_NMAP')

                    name_file_salida = os.path.join(name_dirSalida,"fich_Salida_Nmap_Result.txt")

                    print(colored("Fichero de salida " + name_file_salida ,'green',attrs=['bold']))

                    try:
                        fsal=open(name_file_salida,'a')

                        fsal.write("**************************************" + "\n")
                        fsal.write("         RESULTADOS SCANEO            " + "\n")
                        fsal.write("**************************************" + "\n")
                        fsal.write("                                      " + "\n")
                        fsal.write("**************************************" + "\n")
                        fsal.write("       DATOS GENERALES HOST            " + "\n")
                        fsal.write("**************************************" + "\n")
                        fsal.write("IP: " + IPEntrada + "\n")
                        fsal.write("Estado Host: Arriba,Host levantado" + "\n")

                        for protocol in scaneoIP[IPEntrada].all_protocols():
                            if protocol.lower()=='tcp':
                                proto='TCP'
                            elif protocol.lower()=='udp':
                                proto='UDP'
                            else:
                                proto='XXX'

                            fsal.write("Protocolos:  " + proto + "\n")

                        fsal.write("Nombre del HOST: " + scaneoIP[IPEntrada].hostname()+ "\n")
                        fsal.write("                                                       " + "\n")
                        fsal.write("***********************************************" + "\n")
                        fsal.write("             DATOS DE LOS PUERTOS              " + "\n")
                        fsal.write("***********************************************" + "\n")

                        for protocolo in scaneoIP[IPEntrada].all_protocols():

                            for puertos  in range(21,3390):

                                scaneoIP.scan(IPEntrada,str(puertos))

                                Estado = scaneoIP[IPEntrada][protocolo][int(puertos)]['state']
                                Nombre=scaneoIP[IPEntrada][protocolo][int(puertos)]['name']
                                Producto=scaneoIP[IPEntrada][protocolo][int(puertos)]['product']
                                Version=scaneoIP[IPEntrada][protocolo][int(puertos)]['version']

                                fsal.write("        Puerto:   " + str(puertos)+ "\n")
                                fsal.write("        Estado:   " + str(Estado) + "\n")
                                fsal.write("        Nombre:   " + str(Nombre) + "\n")
                                fsal.write("        Producto: " + str(Producto) + "\n")
                                fsal.write("        Version:  " + str(Version) + "\n")
                                fsal.write("--------------------------------------------"+ "\n")

                        fsal.close()

                    except():
                        print(colored("[-]Error! a la hora de escribir en fichero de salida",'red',attrs=['bold']))
                else:

                    print(colored("**************************************",'green',attrs=['bold']))
                    print(colored("         RESULTADOS SCANEO            ",'green',attrs=['bold']))
                    print(colored("**************************************",'green',attrs=['bold']))
                    print("                                                       ")
                    print(colored("**************************************",'green',attrs=['bold']))
                    print(colored("       DATOS GENERALES HOST            ",'green',attrs=['bold']))
                    print(colored("**************************************",'green',attrs=['bold']))
                    print(colored("IP: ",'green',attrs=['bold']),colored(IPEntrada,'yellow',attrs=['bold']))
                    print(colored("Estado Host: ",'green',attrs=['bold']),colored('Arriba,Host levantado','yellow',attrs=['bold']))

                    print ('protocolos :' + str(scaneoIP[IPEntrada].all_protocols()))        
                    for protocol in scaneoIP[IPEntrada].all_protocols():
                        if protocol.lower()=='tcp':
                            proto='TCP'
                        elif protocol.lower()=='udp':
                            proto='UDP'
                        else:
                            proto='XXX'

                        print(colored("Protocolos:  ",'green',attrs=['bold']),colored (proto,'yellow',attrs=['bold']))

                    print(colored("Nombre del HOST: ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada].hostname(),'yellow',attrs=['bold']))
                    print("                                                       ")

                    for protocolo in scaneoIP[IPEntrada].all_protocols():

                        if resultOPcionPuertos=="2":

                            listaPuertos=['21','22','23','25','53','69','80','109','110','123','125','137','138','139','143','156','389','443','445','531','546','547','993','995','1433','1521','3306','3389','4661','4662','4665']

                            respuesta=input(colored('Mostrar solo puertos abiertos?,S-->SI,N-->NO ','green',attrs=['bold']))
                            print('                                                                                       ')
                            if respuesta.upper()=='S':
                                print(colored("***********************************************",'green',attrs=['bold']))
                                print(colored("             DATOS DE LOS PUERTOS              ",'green',attrs=['bold']))
                                print(colored("***********************************************",'green',attrs=['bold']))
                                print('                                                                                ')
                                contPortOpen=0
                                for puertos  in listaPuertos:

                                    scaneoIP.scan(IPEntrada,puertos)

                                    if scaneoIP[IPEntrada][protocolo][int(puertos)]['state']=='open':

                                        print(colored("        Puerto:   ",'green',attrs=['bold']),colored(puertos,'yellow',attrs=['bold']))
                                        print(colored("        Estado:   ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertos)]['state'],'yellow',attrs=['bold']))
                                        print(colored("        Nombre:   ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertos)]['name'],'yellow',attrs=['bold']))
                                        print(colored("        Producto: ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertos)]['product'],'yellow',attrs=['bold']))
                                        print(colored("        Version:  ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertos)]['version'],'yellow',attrs=['bold']))
                                        print("--------------------------------------------")
                                        contPortOpen=contPortOpen + 1

                                if contPortOpen==0:
                                    print(colored('[-] IP: ' + IPEntrada + ' sin puertos abiertos...','red',attrs=['bold']))

                            else:
                                print(colored("***********************************************",'green',attrs=['bold']))
                                print(colored("             DATOS DE LOS PUERTOS              ",'green',attrs=['bold']))
                                print(colored("***********************************************",'green',attrs=['bold']))
                                print('                                                                                ')

                                for puertos  in listaPuertos:

                                    scaneoIP.scan(IPEntrada,puertos)

                                    print(colored("        Puerto:   ",'green',attrs=['bold']),colored(puertos,'yellow',attrs=['bold']))
                                    print(colored("        Estado:   ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertos)]['state'],'yellow',attrs=['bold']))
                                    print(colored("        Nombre:   ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertos)]['name'],'yellow',attrs=['bold']))
                                    print(colored("        Producto: ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertos)]['product'],'yellow',attrs=['bold']))
                                    print(colored("        Version:  ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertos)]['version'],'yellow',attrs=['bold']))
                                    print("--------------------------------------------")

                        else:

                            puertoElegido=input(colored("POR FAVOR,INDIQUE PUERTO A SCANEAR: ",'green',attrs=['bold']))

                            if len(puertoElegido)==0 or puertoElegido.isdigit()==False:
                                print (colored("[-] NO HA ELEGIDO PUERTO O ESTE NO ES NUMERICO",'red',attrs=['bold']))
                                print("                                                       ")
                                time.sleep(2)
                                exit()

                            else:

                                print(colored("***********************************************",'green',attrs=['bold']))
                                print(colored("             DATOS DE LOS PUERTOS              ",'green',attrs=['bold']))
                                print(colored("***********************************************",'green',attrs=['bold']))
                                print('                                                                                ')

                                scaneoIP.scan(IPEntrada,puertoElegido)

                                print(colored("        Puerto:   ",'green',attrs=['bold']),colored(puertoElegido,'yellow',attrs=['bold']))
                                print(colored("        Estado:   ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertoElegido)]['state'],'yellow',attrs=['bold']))
                                print(colored("        Nombre:   ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertoElegido)]['name'],'yellow',attrs=['bold']))
                                print(colored("        Producto: ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertoElegido)]['product'],'yellow',attrs=['bold']))
                                print(colored("        Version:  ",'green',attrs=['bold']),colored(scaneoIP[IPEntrada][protocolo][int(puertoElegido)]['version'],'yellow',attrs=['bold']))
                                print("--------------------------------------------")

            else:
                print(colored("[-] El host ha scanear no esta levantado ",'red',attrs=['bold']))
                print(colored("HOST STATE: " + hostStatus,'red',attrs=['bold']))
                print("                                                       ")
                time.sleep(2)
    except():
        print(colored("[-] ERROR NO SE HA PODIDO REALIZAR SCAN DE LA IP INDICADA ",'red',attrs=['bold']))
        print("                                                       ")
        time.sleep(3)
        exit()
