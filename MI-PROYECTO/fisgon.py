#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################
# Herramienta para recolectar informacion utilizando
# DNS,Geolocalizacion,nmap y obtener lo METADATOS
# de imagenes y documentos excell, words y ppts
####################################################

####################################################
# Importar modulos
####################################################
import sys
import os
import time
from termcolor import colored
from core.dns_info.obtener_dnsInfo import *
from core.Metadatos.obtenermetaEXCELL import *
from core.Metadatos.obtenermetaPDF    import *
from core.Metadatos.obtenermetaWORD   import *
from core.Metadatos.obtenermetaIMG    import *
from core.Metadatos.obtenermetaPPT    import *
from core.Geolocalizacion.obtenerGeolocaliza import *
from core.Banner_Grabbing.BannerGrabbing import *
from core.nmap.scaneoNMAPsobreIP      import *
from core.DOS.Mi_ataque_dos import *
from core.Fuerza_Bruta.SMTPFuerzaBruta import *
from core.Fuerza_Bruta.FTPFuerzaBruta import *
from core.Fuerza_Bruta.WPFuerzaBruta import *
#ini utilizacion librerias para ataque ssh
#utilizamos esta libreria para ataques ssh ,pero paramiko da problemas
#la version superior a 2.9.0,si no nos fucniona utlizamos el metodos
#pxssh menos eficaz pero no da problemas
#from core.Fuerza_Bruta.SSHFuerzaBruta import *
from core.Fuerza_Bruta.SSHFB import *
#fin utilizacion librerias para ataque ssh
import ipaddress
import socket
from core.nmap import *
from core.IPactivas.FoundIpActive  import *

####################################################
# Se borra las pantalla
####################################################
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

####################################################
# Se valida que la IP objetivo es valida
####################################################
def validaIP(ipObjetivo):
    try:
        ipaddress.ip_address(ipObjetivo)
        return True
    except:
        return False

####################################################
# Se convierte el dominio en ip para poder despues
# validar la IP y luego geolocalizarla
####################################################
def convertirDominioaIP(dominio):
    try:
        direccionIp = socket.gethostbyname(dominio)
        return direccionIp
    except:
        print(colored('[-] Dominio desconocido o no valido','red',attrs=['bold']))
        time.sleep(2)
        borrarPantalla()
        main()

####################################################
# Se accede a nmap para obtener los puertos de la
# IP objetivo.Antes de llamar a nmap, se valida
# dicha IP.
####################################################
def obtenerPuertosNmap():
    borrarPantalla()
    print(colored(' _____ ____   ____    _    _   _ _____ ____    _   _ __  __    _    ____ ' ,'cyan',attrs=['bold']))
    print(colored('| ____/ ___| / ___|  / \  | \ | | ____|  _ \  | \ | |  \/  |  / \  |  _ \ ','cyan',attrs=['bold']))
    print(colored('|  _| \___ \| |     / _ \ |  \| |  _| | |_) | |  \| | |\/| | / _ \ | |_) |','cyan',attrs=['bold']))
    print(colored('| |___ ___) | |___ / ___ \| |\  | |___|  _ <  | |\  | |  | |/ ___ \|  __/ ','cyan',attrs=['bold']))
    print(colored('|_____|____/ \____/_/   \_\_| \_|_____|_| \_\ |_| \_|_|  |_/_/   \_\_|    ','cyan',attrs=['bold']))

    print('                                                                                      ')
    print(colored('1.-)Escaneo NMAP por IP','cyan',attrs=['bold']))
    print(colored('2.-)Escaneo NMAP por Dominio','cyan',attrs=['bold']))
    print(colored('3.-)Escaneo NMAP por Web','cyan',attrs=['bold']))
    print('                                                              ')

    opcionNmap=input(colored('Por favor, elija opcion de escaneo de NMAP: ','green',attrs=['bold']))
    print('                                                              ')

    if opcionNmap=='1':
        ipNmap=input(colored('Por favor,introduzca IP: ','green',attrs=['bold']))

        ipok=validaIP(ipNmap.strip())

        if ipok:
            MiscaneoNMAPsobreIP(ipNmap.strip())
        else:
            print(colored('[-] Ip para escaneo de nmap erronea','red',attrs=['bold']))
            time.sleep(2)
            borrarPantalla()
            main()

    elif opcionNmap=='2':
        dominio=input(colored('Por favor,introduzca Dominio, ejemplo.com: ','green',attrs=['bold']))

        ipDominio=convertirDominioaIP(dominio)
        ipok=validaIP(ipDominio.strip())

        if ipok:
            MiscaneoNMAPsobreIP(ipDominio.strip())
        else:
            print(colored('[-] Dominio para escaneo de nmap erronea','red',attrs=['bold']))
            time.sleep(2)
            borrarPantalla()
            main()

    elif opcionNmap=='3':
        URL=input(colored('Por favor,introduzca Web para escaneo nmap, www.ejemplo.com: ','green',attrs=['bold']))

        ipURL=convertirDominioaIP(URL)
        ipok=validaIP(ipURL.strip())

        if ipok:
            MiscaneoNMAPsobreIP(ipURL.strip())
        else:
            print(colored('[-] web para escaneo de nmap erronea','red',attrs=['bold']))
            time.sleep(2)
            borrarPantalla()
            main()
    else:
        print(colored('[-] Opcion no valida para escaneo de nmap erronea','red',attrs=['bold']))
        time.sleep(2)
        borrarPantalla()
        main()

####################################################
# Se solicita al usuario la ip objetivo o el
# dominio que se quiere geolocalizar,se valida opciones
# y se llama al modulo que geolocaliza el objetivo
####################################################
def obtenerGeolocalizacion():

    borrarPantalla()

    print('                                                     ')
    print(colored('**************************************','green',attrs=['bold']))
    print(colored('********GEOLOCALIZAR OBJETIVO*********','green',attrs=['bold']))
    print(colored('**************************************','green',attrs=['bold']))
    print('                                                     ')
    print(colored('____1.-Geolocalizacion de IP','green',attrs=['bold']))
    print(colored('____2.-Geolocalizacion de dominio','green',attrs=['bold']))
    print('                                                     ')
    opcionGeo=input(colored('Por favor, elija una opcion: ','green',attrs=['bold']))
    print('                                                     ')
    if opcionGeo=="1":
        opcionIP=input(colored('Por favor, introduzca IP: ','green',attrs=['bold']))
        print('                                                     ')
        IPOK=validaIP(opcionIP.strip())
        if IPOK:
            geolocalizaJMM(opcionIP.strip())
        else:
            print(colored('[-] IP para geolocalizar no valida','red',attrs=['bold']))
            time.sleep(2)
            borrarPantalla()
            main()

    elif opcionGeo=="2":
        opcionDominio=input(colored('Por favor, introduzca Dominio: ','green',attrs=['bold']))
        print('                                                     ')

        IPDominio=convertirDominioaIP(opcionDominio.strip())

        IPOKDominio=validaIP(IPDominio.strip())

        if IPOKDominio:

            geolocalizaJMM(IPDominio.strip())
        else:
            print(colored('[-] IP para geolocalizar no valida','red',attrs=['bold']))
            time.sleep(2)
            borrarPantalla()
            main()
    else:
        print(colored('[-] Opcion de geolocalizacion erronea','red',attrs=['bold']))
        time.sleep(2)
        borrarPantalla()
        main()

####################################################
# Se recupera la informacion de los metadatos
# de las imagenes que hay en el directorio imagenes
####################################################
def MetaImg():
    borrarPantalla()
    infoIMG=obtenermetaIMG()
    if infoIMG != None :
        print("\n")
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print(colored("      Información general de la imagen " 'blue',attrs=['bold']))
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print("\n")
        #Obtenemos el tag y su valor
        try:
            infoGPS=False
            for (tag,value) in infoIMG.items():

                if 'GPSInfo' in str(TAGS.get(tag)):
                    infoGPS=True
                    print (colored(str(TAGS.get(tag)),'blue',attrs=['bold']) +  " = " + colored(str(value),'yellow',attrs=['bold']))

                else:
                    print (colored(str(TAGS.get(tag)),'blue',attrs=['bold']) +  " = " + colored(str(value),'yellow',attrs=['bold']))
            if infoGPS==False:
                print(colored("Sin informacion GPS",'blue',attrs=['bold']))
        except AttributeError as e:
            print (colored('[-] ha producido un error:  %s' % e ,'red',attrs=['bold']))
        except:
            print (colored('[-] Se ha producido un error inesperado','red',attrs=['bold']))

    seguir='n'
    while seguir != 's':
        print('                                                                    ')
        seguir=input(colored('Por favor, presione tecla s para continuar: ','green',attrs=['bold']))
        if seguir.lower()=='s':
            time.sleep(0.5)
            borrarPantalla()
            main()

####################################################
# Se recupera la informacion de los metadatos
# de las documentos word que hay en el directorio
# de trabajo Docu_WORDs
####################################################
def MetaWord():
    borrarPantalla()
    infoWORD=obtenermetaWORD()
    if infoWORD != None :
        #La imprimimos por pantalla
        print("\n")
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print(colored("      Información general del word " ,'blue',attrs=['bold']))
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print("\n")
        #Obtenemos los datos del documento word
        try:
            print (colored("[+] " "Autor",'blue',attrs=['bold']) + " = " + colored(infoWORD.author,'yellow',attrs=['bold']))
            print (colored("[+] " "Categoria",'blue',attrs=['bold']) + " = " + colored(infoWORD.category,'yellow',attrs=['bold']))
            print (colored("[+] " "Comentarios",'blue',attrs=['bold']) + " = " + colored(infoWORD.comments,'yellow',attrs=['bold']))
            print (colored("[+] " "Estado del comentario",'blue',attrs=['bold']) + " = " + colored(infoWORD.content_status,'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha de creacion",'blue',attrs=['bold']) + " = " + colored(str(infoWORD.created),'yellow',attrs=['bold']))
            print (colored("[+] " "Identificador",'blue',attrs=['bold']) + " = " + colored(infoWORD.identifier,'yellow',attrs=['bold']))
            print (colored("[+] " "Keywords",'blue',attrs=['bold']) + " = " + colored(infoWORD.keywords,'yellow',attrs=['bold']))
            print (colored("[+] " "Idioma",'blue',attrs=['bold']) + " = " + colored(infoWORD.language,'yellow',attrs=['bold']))
            print (colored("[+] " "Autor Ultima Modificacion",'blue',attrs=['bold']) + " = " + colored(infoWORD.last_modified_by,'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha ultima impresion",'blue',attrs=['bold']) + " = " + colored(str(infoWORD.last_printed),'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha Modificacion",'blue',attrs=['bold']) + " = " + colored(str(infoWORD.modified),'yellow',attrs=['bold']))
            print (colored("[+] " "Numero de Revision",'blue',attrs=['bold']) + " = " + colored(infoWORD.revision,'yellow',attrs=['bold']))
            print (colored("[+] " "subject",'blue',attrs=['bold']) + " = " + colored(infoWORD.subject,'yellow',attrs=['bold']))
            print (colored("[+] " "Titulo",'blue',attrs=['bold']) + " = " + colored(infoWORD.title,'yellow',attrs=['bold']))
            print (colored("[+] " "Version",'blue',attrs=['bold']) + " = " + colored(infoWORD.version,'yellow',attrs=['bold']))

        except:
            print (colored('[-]Se ha producido un error inesperado','red',attrs=['bold']))

    seguir='n'
    while seguir != 's':
        print('                                                                    ')
        seguir=input(colored('Por favor, presione tecla s para continuar: ','green',attrs=['bold']))
        if seguir.lower()=='s':
            time.sleep(0.5)
            borrarPantalla()
            main()

####################################################
# Se recupera la informacion de los metadatos
# de las documentos excell que hay en el directorio
# de trabajo Docu_EXCELLs
####################################################
def MetaExcell():
    borrarPantalla()
    infoEXCELL=obtenermetaEXCELL()
    if infoEXCELL != None:
        print("\n")
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print(colored("      Información general del excell " ,'blue',attrs=['bold']))
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print("\n")
        try:
            print (colored("[+] " "Autor",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.creator,'yellow',attrs=['bold']))
            print (colored("[+] " "Descripcion",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.description,'yellow',attrs=['bold']))
            print (colored("[+] " "subject",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.subject,'yellow',attrs=['bold']))
            print (colored("[+] " "Categoria",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.category,'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha de creacion",'blue',attrs=['bold']) + " = " + colored(str(infoEXCELL.created),'yellow',attrs=['bold']))
            print (colored("[+] " "contenido Estado",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.contentStatus,'yellow',attrs=['bold']))
            print (colored("[+] " "Keywords",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.keywords,'yellow',attrs=['bold']))
            print (colored("[+] " "Idioma",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.language,'yellow',attrs=['bold']))
            print (colored("[+] " "Autor Ultima Modificacion",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.last_modified_by,'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha ultima impresion",'blue',attrs=['bold']) + " = " + colored(str(infoEXCELL.lastPrinted),'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha Modificacion",'blue',attrs=['bold']) + " = " + colored(str(infoEXCELL.modified),'yellow',attrs=['bold']))
            print (colored("[+] " "Numero de Revision",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.revision,'yellow',attrs=['bold']))
            #print (colored("[+] " "subject",'blue',attrs=['bold']) + " = " + colored(info_documento.subject,'yellow',attrs=['bold']))
            print (colored("[+] " "Titulo",'blue',attrs=['bold']) + " = " + colored(infoEXCELL.title,'yellow',attrs=['bold']))
            #print (colored("[+] " "Version",'blue',attrs=['bold']) + " = " + colored(info_documento.version,'yellow',attrs=['bold']))

        except:
            print (colored('[-] Se ha producido un error inesperado','red',attrs=['bold']))
    seguir='n'
    while seguir != 's':
        print('                                                                    ')
        seguir=input(colored('Por favor, presione tecla s para continuar: ','green',attrs=['bold']))
        if seguir.lower()=='s':
            time.sleep(0.5)
            borrarPantalla()
            main()

####################################################
# Se recupera la informacion de los metadatos
# de las documentos PDF que hay en el directorio
# de trabajo Docu_PDFs
####################################################
def MetaPDF():
    borrarPantalla()
    infoPDF=obtenermetaPDF()
    if infoPDF != None :
        print("\n")
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print(colored("      Información general del pdf " ,'blue',attrs=['bold']))
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print("\n")
        #Obtenemos el tag y su valor
        try:
            for (metadatopdf,valor) in infoPDF.items():
                print (colored("[+] " + metadatopdf,'blue',attrs=['bold']) + " = " + colored(valor,'yellow',attrs=['bold']))

        except:
            print (colored('[-] Se ha producido un error inesperado','red',attrs=['bold']))

    seguir='n'
    while seguir != 's':
        print('                                                                    ')
        seguir=input(colored('Por favor, presione tecla s para continuar: ','green',attrs=['bold']))
        if seguir.lower()=='s':
            time.sleep(0.5)
            borrarPantalla()
            main()

####################################################
# Se recupera la informacion de los metadatos
# de las documentos PDF que hay en el directorio
# de trabajo Docu_PDFs
####################################################
def MetaPPT():
    borrarPantalla()
    infoPPT=obtenermetaPPT()
    if infoPPT != None:
        print("\n")
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print(colored("      Información general del ppt " ,'blue',attrs=['bold']))
        print(colored("###############################################################################",'blue',attrs=['bold']))
        print("\n")
        #Obtenemos los datos del documento PPT
        try:
            print (colored("[+] " "Autor",'blue',attrs=['bold']) + " = " + colored(infoPPT.author,'yellow',attrs=['bold']))
            print (colored("[+] " "Categoria",'blue',attrs=['bold']) + " = " + colored(infoPPT.category,'yellow',attrs=['bold']))
            print (colored("[+] " "Comentarios",'blue',attrs=['bold']) + " = " + colored(infoPPT.comments,'yellow',attrs=['bold']))
            print (colored("[+] " "Estado del comentario",'blue',attrs=['bold']) + " = " + colored(infoPPT.content_status,'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha de creacion",'blue',attrs=['bold']) + " = " + colored(str(infoPPT.created),'yellow',attrs=['bold']))
            print (colored("[+] " "Identificador",'blue',attrs=['bold']) + " = " + colored(infoPPT.identifier,'yellow',attrs=['bold']))
            print (colored("[+] " "Keywords",'blue',attrs=['bold']) + " = " + colored(infoPPT.keywords,'yellow',attrs=['bold']))
            print (colored("[+] " "Idioma",'blue',attrs=['bold']) + " = " + colored(infoPPT.language,'yellow',attrs=['bold']))
            print (colored("[+] " "Autor Ultima Modificacion",'blue',attrs=['bold']) + " = " + colored(infoPPT.last_modified_by,'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha ultima impresion",'blue',attrs=['bold']) + " = " + colored(str(infoPPT.last_printed),'yellow',attrs=['bold']))
            print (colored("[+] " "Fecha Modificacion",'blue',attrs=['bold']) + " = " + colored(str(infoPPT.modified),'yellow',attrs=['bold']))
            print (colored("[+] " "Numero de Revision",'blue',attrs=['bold']) + " = " + colored(infoPPT.revision,'yellow',attrs=['bold']))
            print (colored("[+] " "subject",'blue',attrs=['bold']) + " = " + colored(infoPPT.subject,'yellow',attrs=['bold']))
            print (colored("[+] " "Titulo",'blue',attrs=['bold']) + " = " + colored(infoPPT.title,'yellow',attrs=['bold']))
            print (colored("[+] " "Version",'blue',attrs=['bold']) + " = " + colored(infoPPT.version,'yellow',attrs=['bold']))

        except:
            print (colored('[-] Se ha producido un error inesperado','red',attrs=['bold']))

    seguir='n'
    while seguir != 's':
        print('                                                                    ')
        seguir=input(colored('Por favor, presione tecla s para continuar: ','green',attrs=['bold']))
        if seguir.lower()=='s':
            time.sleep(0.5)
            borrarPantalla()
            main()

####################################################
# Se accede al modulo de banner grabbing para
# buscar versiones vulnerables
####################################################
def bannerGrabinng():
    borrarPantalla()

    print(colored("******************************************",'green',attrs=['bold']))
    print(colored("************BANNER-GRABBING***************",'green',attrs=['bold']))
    print(colored("******************************************",'green',attrs=['bold']))
    print("                                                      ")

    ipBanner=input(colored("Por favor, introduzca Ip para Banner-Grabbing: ",'green',attrs=['bold']))
    ipBannerOK=validaIP(ipBanner.strip())

    if ipBannerOK:
        bannerGrabinngMain(ipBanner.strip())
    else:
        print(colored("[-] Ip para Banner-Grabbing NO valida",'red',attrs=['bold']))
        time.sleep(0.5)
        borrarPantalla()

####################################################
# Se realiza un ataque de denegacion de servicio
# el ataque necesita privilegios de administrador
####################################################
def DOS():
    ataqueDOS()

####################################################
# Se realiza un ataque de fuerza Bruta, se presenta
# un menu para realziar ataques al puerto 21,22,25
####################################################
def fuerzaBruta():
    borrarPantalla()
    print(colored("****************************",'green',attrs=['bold']))
    print(colored("****ATAQUES FUERZA BRUTA****",'green',attrs=['bold']))
    print(colored("****************************",'green',attrs=['bold']))
    print(colored("1.-Ataque protocolo FTP",'green',attrs=['bold']))
    print(colored("2.-Ataque protocolo SSH",'green',attrs=['bold']))
    print(colored("3.-Ataque protocolo SMTP-cuentas GMAIL",'green',attrs=['bold']))
    print(colored("4.-Ataque obtener usuarios WordPress",'green',attrs=['bold']))
    print("                                                       ")
    opcionFB=input(colored("Por favor, elija una de la opciones del menu: ",'green',attrs=['bold']))
    if opcionFB=='1':
        IpFtp=input(colored("Introduzca la IP a escanear: ",'green',attrs=['bold']))
        ipftpOK=validaIP(IpFtp.strip())
        if ipftpOK:
            FtpFb(IpFtp.strip())
        else:
            print(colored("[-] IP no valida para ataque de fuerza bruta FTP",'red',attrs=['bold']))
            time.sleep(3)
            borrarPantalla()
            main()

    elif opcionFB=='2':
        IpSsh=input(colored("Introduzca la IP a escanear: ",'green',attrs=['bold']))
        ipsshOK=validaIP(IpSsh.strip())
        if ipsshOK:
           SshFb(IpSsh.strip())
        else:
            print(colored("[-] IP no valida para ataque de fuerza bruta SSH",'red',attrs=['bold']))
            time.sleep(3)
            borrarPantalla()
            main()
    elif opcionFB=='3':
            SmtpFb()
    elif opcionFB=='4':
            WpFb()
    else:
        print(colored("[-] Opcion para ataque de Fuerza Bruta no valida",'red',attrs=['bold']))
        time.sleep(3)
        borrarPantalla()
        main()

####################################################
# Se recupera la informacion de los dsn del
# objetivo.Se solicita dominio del objetivo
####################################################
def obtenerDnsInfo():

    borrarPantalla()

    print(colored("****************************",'green',attrs=['bold']))
    print(colored("*******DNS INFORMACION******",'green',attrs=['bold']))
    print(colored("****************************",'green',attrs=['bold']))
    print("                                                       ")
    opcionDnsInfo=input(colored("Por favor, introduzca dominio objetivo, ejemplo.com: ",'green',attrs=['bold']))
    if len(opcionDnsInfo)==0:
        print(colored("[-]Dominio no valido",'red',attrs=['bold']))
        time.sleep(3)
        borrarPantalla()
        main()
    else:
        borrarPantalla()
        resolverDNS(opcionDnsInfo)

####################################################
# Se recupera los metadatos
# se genera menu para elegir el tipo de documentos
# Imagenes,word,excell,ppt
####################################################
def obtenerMetadatos():

    borrarPantalla()

    print(colored("******************************************",'cyan',attrs=['bold']))
    print(colored("*********MENU RECOLECTAR METADATOS********",'cyan',attrs=['bold']))
    print(colored("******************************************",'cyan',attrs=['bold']))
    print("                                                      ")
    print(colored("___ 1.-)Metadatos de Imagenes",'green',attrs=['bold']))
    print(colored("___ 2.-)Metadatos de documentos Word",'green',attrs=['bold']))
    print(colored("___ 3.-)Metadatos de documentos Excell",'green',attrs=['bold']))
    print(colored("___ 4.-)Metadatos de documentos PPTs",'green',attrs=['bold']))
    print(colored("___ 5.-)Metadatos de documentos PDF",'green',attrs=['bold']))
    print(colored("___ 6.-)Volver al menu principal",'green',attrs=['bold']))
    print("                                                      ")

    opcionMeta=input(colored("Por favor, elija una de las opciones: ",'green',attrs=['bold']))

    print("                                                      ")
    if opcionMeta=="1":
        MetaImg()
    elif opcionMeta=="2":
        MetaWord()
    elif opcionMeta=="3":
        MetaExcell()
    elif opcionMeta=="4":
        MetaPPT()
    elif opcionMeta=="5":
        MetaPDF()
    elif opcionMeta=="6":
        print(colored("Vuelta menu principal en 3,2,1...",'green',attrs=['bold']))
        time.sleep(2)
        borrarPantalla()
        main()
    else:
        print(colored("[-]Opcion no valida, por favor intentelo de nuevo",'red',attrs=['bold']))
        time.sleep(3)
        borrarPantalla()
        main()

####################################################
# Menu para analizar vulnerabilidades
#####################################################
def analisiVul():
    borrarPantalla()

    print(colored("******************************************",'cyan',attrs=['bold']))
    print(colored("**********MENU VULNERABILIDADES***********",'cyan',attrs=['bold']))
    print(colored("******************************************",'cyan',attrs=['bold']))
    print("                                                      ")

    print(colored("___ 1.-)Fuerza Bruta",'green',attrs=['bold']))
    print(colored("___ 2.-)Dos(Denegacion de servicio)",'green',attrs=['bold']))
    print(colored("___ 3.-)Banner-Grabbing",'green',attrs=['bold']))
    print(colored("___ 4.-)Volver menu principal",'green',attrs=['bold']))
    print("                                                      ")

    opcionVuln=input(colored("Por favor, elija una de las opciones: ",'green',attrs=['bold']))

    print("                                                      ")
    if opcionVuln=="1":
        fuerzaBruta()
    elif opcionVuln=="2":
        DOS()
    elif opcionVuln=="3":
        bannerGrabinng()
    elif opcionVuln=="4":
        print(colored("Vuelta menu principal en 3,2,1...",'green',attrs=['bold']))
        time.sleep(2)
        borrarPantalla()
        main()
    else:
        print(colored("[-]Opcion no valida, por favor intentelo de nuevo",'red',attrs=['bold']))
        time.sleep(3)
        borrarPantalla()
        main()
####################################################
# Menu para recolectar informacion, se debe de
# elegir una de las opciones
####################################################
def recolectarInfo():

    borrarPantalla()

    print(colored("******************************************",'cyan',attrs=['bold']))
    print(colored("********MENU RECOLECTAR INFORMACION*******",'cyan',attrs=['bold']))
    print(colored("******************************************",'cyan',attrs=['bold']))
    print("                                                      ")

    print(colored("___ 1.-)DNS Info",'green',attrs=['bold']))
    print(colored("___ 2.-)Geolocalizacion del objetivo",'green',attrs=['bold']))
    print(colored("___ 3.-)Obtecion de Metadatos",'green',attrs=['bold']))
    print(colored("___ 4.-)Obtencion de puertos por nmap",'green',attrs=['bold']))
    print(colored("___ 5.-)Descubrir Ips activas en la red escaneada",'green',attrs=['bold']))
    print(colored("___ 6.-)Volver menu principal",'green',attrs=['bold']))
    print("                                                      ")

    opcionReco=input(colored("Por favor, elija una de las opciones: ",'green',attrs=['bold']))

    print("                                                      ")
    if opcionReco=="1":
        obtenerDnsInfo()
    elif opcionReco=="2":
        obtenerGeolocalizacion()
    elif opcionReco=="3":
        obtenerMetadatos()
    elif opcionReco=="4":
        obtenerPuertosNmap()
    elif opcionReco=="5":
        IPactiv()
    elif opcionReco=="6":
        print(colored("Vuelta menu principal en 3,2,1...",'green',attrs=['bold']))
        time.sleep(2)
        borrarPantalla()
        main()
    else:
        print(colored("[-]Opcion no valida, por favor intentelo de nuevo",'red',attrs=['bold']))
        time.sleep(3)
        borrarPantalla()
        main()


####################################################
# Menu principal, se elige entre recolectar
# informacion y explotar vulnerabilidad
####################################################
def main():

    borrarPantalla()

    print (colored('************************************************************************','cyan',attrs=['bold']))
    print (colored('            _____ ___ ____   ____  ___  _   _      ','cyan',attrs=['bold']))
    print (colored('           |  ___|_ _/ ___| / ___|/ _ \| \ | |     ','cyan',attrs=['bold']))
    print (colored('           | |_   | |\___ \| |  _| | | |  \| |     ','cyan',attrs=['bold']))
    print (colored('           |  _|  | | ___) | |_| | |_| | |\  |     ','cyan',attrs=['bold']))
    print (colored('           |_|   |___|____/ \____|\___/|_| \_|     ','cyan',attrs=['bold']))
    print (colored('                                                 ' ,'cyan',attrs=['bold']))
    print (colored('************************************************************************','cyan',attrs=['bold']))
    print (colored('    __  ___                    ____       _            _             __','cyan',attrs=['bold']))
    print (colored('   /  |/  /__  ____  __  __   / __ \_____(_)___  _____(_)___  ____ _/ /','cyan',attrs=['bold']))
    print (colored('  / /|_/ / _ \/ __ \/ / / /  / /_/ / ___/ / __ \/ ___/ / __ \/ __ `/ / ','cyan',attrs=['bold']))
    print (colored(' / /  / /  __/ / / / /_/ /  / ____/ /  / / / / / /__/ / /_/ / /_/ / / ','cyan',attrs=['bold']))
    print (colored('/_/  /_/\___/_/ /_/\__,_/  /_/   /_/  /_/_/ /_/\___/_/ .___/\__,_/_/  ','cyan',attrs=['bold']))
    print (colored('                                                    /_/               ','cyan',attrs=['bold']))
    print(colored("*************************************************************************",'cyan',attrs=['bold']))
    print("                                                      ")

    print(colored("___ 1.-)Recoleccion de Informacion",'green',attrs=['bold']))
    print(colored("___ 2.-)Analisis de Vulnerabilidades",'green',attrs=['bold']))
    print(colored("___ 3.-)Salir del Modulo",'green',attrs=['bold']))
    print("                                                      ")

    opcion=input(colored("Por favor, elija una de las opciones: ",'green',attrs=['bold']))

    print("                                                      ")

    if opcion=="1":
        borrarPantalla()
        recolectarInfo()

    elif opcion=="2":
        borrarPantalla()
        analisiVul()

    elif opcion=="3":
        print(colored("Gracias por su visita, hasta pronto.....",'green',attrs=['bold']))

    else:
        print(colored("[-]Opcion no valida, por favor intentelo de nuevo",'red',attrs=['bold']))
        time.sleep(3)
        borrarPantalla()
        main()

####################################################
# Llamada al menu principal
####################################################
if __name__ == "__main__":
    main()
