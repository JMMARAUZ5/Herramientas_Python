#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################################################################
#                           BANNER GRABBING                                      #
#  Se pasa por parametro la ip objetivo  yse dispone de dos ficheros             #
#  uno con un listado de puertos y otro con las vulnerabilidades a estudiar      #
#  se valida cada vulnerabilidad para cada puerto                                #
##################################################################################
import socket
import sys
import os
import time
from termcolor import colored
import nmap

##################################################################
# Leemos fichero de vulnerabilidades                             #
#################################################################
def leerFichVuln(fichEnt):
    leerFichV=open(fichEnt,'r').readlines()
    leerFichVFinal=(vulnera.strip() for vulnera in leerFichV)
    return leerFichVFinal

##################################################################
# Validamos que el fichero de vulnerabilidades exista            #
# en la ruta indicada,si no exite e devuelve error               #
#################################################################
def validarFicheroVuln(dir,fichEntVuln):
    name_dir = os.path.join(os.path.dirname(__file__),dir)

    if os.path.isdir(name_dir):

        name_file = os.path.join(name_dir,fichEntVuln)

        if not os.path.isfile(name_file):
            print(colored("[-] No existe el fichero de vulnerabilidades indicado,por favor revise nombre fichero",'red',attrs=['bold']))
            exit()
        elif os.stat(name_file).st_size == 0:
            print(colored("[-] El fichero de puertos esta vacio",'red',attrs=['bold']))
            exit()
        else:
            leerVuln=leerFichVuln(name_file)
            return leerVuln
    else:
        print(colored("[-] El directorio no existe,por favor revise nombre de directorio, debe ser ficherosEnt",'red',attrs=['bold']))
        exit()

################################################################
# Funcion para obtener el banner de un puerto para una IP dada #
# establecemos una relacion cliente servidor utilizando socket #
# creamos objeto socket con la funcion socket e indicamos el   #
# el protocolo en este caso AF_INET y el tipo de comunicacion  #
# SOCK_STREAM-->protocolo orientado a comunicaciones TCP       #
# recv-->1024 cantidad de datos maxima que se puede recibir de #
# una vez                                                      #
################################################################
def obtenerBanner(ipEnt,puerto):

  try:
      conexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      socket.setdefaulttimeout(900.0)
      conexion.connect((ipEnt,int(puerto)))
      #socket.setdefaulttimeout(900.0)

      banner = conexion.recv(1024)

      print(colored('banner obtenido: ' + str(banner).strip(),'green',attrs=['bold']))

      leerVuln=validarFicheroVuln("ficherosEnt","vulnerable-port" + puerto + ".txt")
      for vulnerabilidad in leerVuln:

          if str(vulnerabilidad).strip() in str(banner).strip():
              print (colored('***************************************','green',attrs=['bold']))
              print (colored('[+] EL BANNER ES VULNERABLE','green',attrs=['bold']))
              print (colored('[+] IP            : ' + ipEnt,'green',attrs=['bold']))
              print (colored('[+] PUERTO        : ' + puerto,'green',attrs=['bold']))
              print (colored('[+] VULNERABILIDAD: ' + vulnerabilidad,'green',attrs=['bold']))
              print (colored('***************************************','green',attrs=['bold']))
#          else:
#              print (colored('***************************************','red',attrs=['bold']))
#              print (colored('[-] EL BANNER NO ES VULNERABLE','red',attrs=['bold']))
#              print (colored('[-] IP            : ' + ipEnt,'red',attrs=['bold']))
#              print (colored('[-] PUERTO        : ' + puerto,'red',attrs=['bold']))
#              print (colored('***************************************','red',attrs=['bold']))
      conexion.close()
  except ConnectionRefusedError as e:
      print(colored('***************************************','red',attrs=['bold']))
      print(colored("CONEXION REFUSED",'red',attrs=['bold']))
      print(colored("PUERTO: " + puerto ,'red',attrs=['bold']))
      print (colored('***************************************','red',attrs=['bold']))
  except ConnectionResetError as e:
      print (colored('***************************************','red',attrs=['bold']))
      print(colored("CONEXION RESET ERROR",'red',attrs=['bold']))
      print(colored("PUERTO: " + puerto ,'red',attrs=['bold']))
      print (colored('***************************************','red',attrs=['bold']))
  except socket.timeout as e:
      print (colored('***************************************','red',attrs=['bold']))
      print(colored("TIMEOUT EN CONEXION",'red',attrs=['bold']))
      print(colored("PUERTO: " + puerto ,'red',attrs=['bold']))
      print (colored('***************************************','red',attrs=['bold']))
  #except:
    #  print(colored("ERROR INESPERADO AL INTENTAR CONEXION AL SOCKET",'red',attrs=['bold']))
     # exit()

##################################################################
# Validamos que el la ip y elpuerto, esten abietos               #
#################################################################
def nmapOpenPort(ip,puerto):
    nm=nmap.PortScanner()
    try:
        nm.scan(ip,puerto)
        if nm[ip]['tcp'][int(puerto)]['state']=='open':
            return True
        else:
            return False
    except:
        print(colored('Error al realizar nmap scan de la ip: ' + ip + ' Puerto: ' + puerto,'red',attrs=['bold']))

##################################################################
# Vamos al menu principal se pide IP objetivo                    #
# Se validan que los ficheros existan.                           #
# se valida que los ficheros no esten vacios y se realiza        #
# mediante la api socket conexion con la maquina objetivo para   #
# recuperar el banner y validarlo para cada vulnerabilidad       #
# y para cada uno de los puertos                                 #
# solo lo haremos si el puerto esta abierto
##################################################################
def bannerGrabinngMain(ip):

   listPorts=['21','22','23','25','80','443','445']

   for port in listPorts:
       OpenPort=nmapOpenPort(ip,port)
       if OpenPort:
           print('                                                               ')
           print(colored('[+] Puerto ' + port + ' para ip ' + ip + ' esta abierto','green',attrs=['bold']))
           print(colored('[+] Se realiza Banner-Grabbing','green',attrs=['bold']))

           obtenerBanner(ip,port)
       else:
           print(colored('[-] Puerto ' + port + ' para ip ' + ip + ' no esta abierto','red',attrs=['bold']))
           print(colored('[-] No se realiza Banner-Grabbing','red',attrs=['bold']))
