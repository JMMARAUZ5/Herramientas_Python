#/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################
# Herramienta para geolocalizar la ip objetivo
# se devuelven los datos como longuitud y latitud
# asi como, ciudad,codigo postal etc...
# Tras la geolocalizacion, se da la posibilidad de
# acceder a google maps para ver la localizacion de
# en maps del objetivo.
# La informacion se puede mostrar por pantalla o
# se puede enviar a un fichero de salida, que se
# almacena en el directorio salidaGeo
####################################################

####################################################
# Importar modulos
####################################################
import sys
import os
from termcolor import colored
from urllib import request
import json
import webbrowser

####################################################
# Se borra las pantalla
####################################################
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

####################################################
# Se indica el navegador que queremos utilizar
# se abre en dicho navegador la URL
####################################################
def abrirUrl(url,navegador):
    try:
        nav=webbrowser.get(navegador)
        nav.open(url)
    except webbrowser.Error:
        print(colored("[-] No se ha podido abrir la url indicada",'red',attrs=['bold']))

####################################################
# Se escribe los resultado en un fichero, dicho
# fichero estara en el directorio salidaGeo
# se valida que el directorio exista
####################################################
def escribirEnFich(resultados,ip):
    name_dirSal =os.path.join(os.path.dirname(__file__),'salidaGeo')
    if not os.path.isdir(name_dirSal):
        print(colored("[-] No existe el directorio salidaGeo",'red',attrs=['bold']))
        exit()
    else:
        name_file = os.path.join(name_dirSal,'Resultado_Geolocalizacion_' + ip + '.txt')

        try:
            fichSal=open(name_file,'a')
            fichSal.write('Informacion sobre la IP Objetivo: ' + ip + "\n")
            fichSal.write('=================================================' + "\n")
            fichSal.write('                                                 ' + "\n")
            if 'query' in  resultados:
                fichSal.write('IP..................:' + resultados['query'] + "\n")
            if 'status' in  resultados:
                fichSal.write('Estado..............:' + resultados['status']+ "\n")
            if 'continent' in  resultados:
                fichSal.write('Continente..........:' + resultados['continent']+ "\n")
            if 'country' in  resultados:
                fichSal.write('Pais................:' + resultados['country']+ "\n")
            if 'countryCode' in  resultados:
                fichSal.write('Codigo de Pais......:' + resultados['countryCode']+ "\n")
            if 'region' in  resultados:
                fichSal.write('Region..............:' + resultados['region']+ "\n")
            if 'regionName' in  resultados:
                fichSal.write('Nombre de la Region.:' + resultados['regionName']+ "\n")
            if 'city' in  resultados:
                fichSal.write('Ciudad..............:' + resultados['city']+ "\n")
            if 'zip' in  resultados:
                fichSal.write('Zip.................:' + resultados['zip']+ "\n")
            if 'lat' in  resultados:
                fichSal.write('Latitud.............:' + str(resultados['lat']) + "\n")
            if 'lon' in  resultados:
                fichSal.write('Longuitud...........:' + str(resultados['lon']) + "\n")
            if 'timezone' in  resultados:
                fichSal.write('Zona Horaria........:' + resultados['timezone']+ "\n")
            if 'isp' in  resultados:
                fichSal.write('ISP.................:' + resultados['isp']+ "\n")
            if 'org' in  resultados:
                fichSal.write('Organizacion........:' + resultados['org']+ "\n")
            if 'as' in  resultados:
                fichSal.write('As..................:' + resultados['as']+ "\n")

            fichSal.write('URL site Maps.......:' + 'http://www.google.com/maps/place/' + str(resultados['lat']) + ',' + str(resultados['lon']) + '/@' + str(resultados['lat']) + ',' + str(resultados['lon']) + ',17z'+ "\n")

            fichSal.close()
            url='http://www.google.com/maps/place/' + str(resultados['lat']) + ',' + str(resultados['lon']) + '/@' + str(resultados['lat']) + ',' + str(resultados['lon']) + ',17z'

            print('                                                              ')
            opcionURL=input(colored('Quiere ver la URL de Google Maps en el navegador de firefox? ,Si=S o No=N ','blue',attrs=['bold']))

            if opcionURL.upper()=='S':
                print(colored('El navegador utilizado por defecto es firefox','blue',attrs=['bold']))
                navegador = "firefox"
                abrirUrl(url,navegador)
        except FileNotFoundError:
            print(colored('Error al escribir el fichero,fichero no encontrado','red',attrs=['bold']))
        except:
            print(colored('Error al escribir el fichero','red',attrs=['bold']))

##########################################################
# Se indica el navegador que queremos utilizar
# se abre en dicho navegador la URL
####################################################
def abrirUrl(url,navegador):
    try:
        nav=webbrowser.get(navegador)
        nav.open(url)
    except webbrowser.Error:
        print(colored("[-]No se ha podido abrir la url indicada",'red',attrs=['bold']))
        exit()
##############################################
# Modulo principal
####################################################
def geolocalizaJMM(IpVictima):

    borrarPantalla()

    print(colored('   ____ _____ ___  _     ___   ____    _    _     ___ _____   _     ','blue',attrs=['bold']))
    print(colored('  / ___| ____/ _ \| |   / _ \ / ___|  / \  | |   |_ _|__  /  / \    ','blue',attrs=['bold']))
    print(colored(' | |  _|  _|| | | | |  | | | | |     / _ \ | |    | |  / /  / _ \   ','blue',attrs=['bold']))
    print(colored(' | |_| | |__| |_| | |__| |_| | |___ / ___ \| |___ | | / /_ / ___ \  ','blue',attrs=['bold']))
    print(colored('  \____|_____\___/|_____\___/ \____/_/   \_\_____|___/____/_/   \_\ ','blue',attrs=['bold']))
    print('                                                                            ')

    URL = 'http://ip-api.com/json/{}'

    req = request.Request(URL.format(IpVictima), headers={'User-Agent': 'My User Agent 1.0' })

    respuesta = request.urlopen(req)
#Validamos si la respuesta ha sido correcta
    if respuesta.code ==200:

        datos=respuesta.read().decode('utf-8')
#Convertimos la clase str a clase dict,para poder recorrer el diccionario y obtener
#los distintos valores para ello utilizamos la clase json y el metodo loads
        datosConvert=json.loads(datos)

        if datosConvert['status'] == 'success':
            opcionOutput=input(colored('¿Desea enviar resultado a fichero, S-->SI,N-->NO ? ','green',attrs=['bold']))
            if opcionOutput.upper()=='S':
                print(colored('El fichero se alamacena en el directorio llamado salidaGeo','green',attrs=['bold']))
                escribirEnFich(datosConvert,IpVictima)
            else:
                print('                                                                            ')
                print(colored('Informacion sobre la IP Objetivo: ' + IpVictima,'blue',attrs=['bold']))
                print(colored('=================================================','blue',attrs=['bold']))
                print('                                                                            ')
                if 'query' in  datosConvert:
                    print(colored('IP..................:','blue',attrs=['bold']),colored(datosConvert['query'],'yellow',attrs=['bold']))
                if 'status' in  datosConvert:
                    print(colored('Estado..............:','blue',attrs=['bold']),colored(datosConvert['status'],'yellow',attrs=['bold']))
                if 'continent' in  datosConvert:
                    print(colored('Continente..........:','blue',attrs=['bold']),colored(datosConvert['continent'],'yellow',attrs=['bold']))
                if 'country' in  datosConvert:
                    print(colored('Pais................:','blue',attrs=['bold']),colored(datosConvert['country'],'yellow',attrs=['bold']))
                if 'countryCode' in  datosConvert:
                    print(colored('Codigo de Pais......:','blue',attrs=['bold']),colored(datosConvert['countryCode'],'yellow',attrs=['bold']))
                if 'region' in  datosConvert:
                    print(colored('Region..............:','blue',attrs=['bold']),colored(datosConvert['region'],'yellow',attrs=['bold']))
                if 'regionName' in  datosConvert:
                    print(colored('Nombre de la Region.:','blue',attrs=['bold']),colored(datosConvert['regionName'],'yellow',attrs=['bold']))
                if 'city' in  datosConvert:
                    print(colored('Ciudad..............:','blue',attrs=['bold']),colored(datosConvert['city'],'yellow',attrs=['bold']))
                if 'zip' in  datosConvert:
                    print(colored('Zip.................:','blue',attrs=['bold']),colored(datosConvert['zip'],'yellow',attrs=['bold']))
                if 'lat' in  datosConvert:
                    print(colored('Latitud.............:','blue',attrs=['bold']),colored(datosConvert['lat'],'yellow',attrs=['bold']))
                if 'lon' in  datosConvert:
                    print(colored('Longuitud...........:','blue',attrs=['bold']),colored(datosConvert['lon'],'yellow',attrs=['bold']))
                if 'timezone' in  datosConvert:
                    print(colored('Zona Horaria........:','blue',attrs=['bold']),colored(datosConvert['timezone'],'yellow',attrs=['bold']))
                if 'isp' in  datosConvert:
                    print(colored('ISP.................:','blue',attrs=['bold']),colored(datosConvert['isp'],'yellow',attrs=['bold']))
                if 'org' in  datosConvert:
                    print(colored('Organizacion........:','blue',attrs=['bold']),colored(datosConvert['org'],'yellow',attrs=['bold']))
                if 'as' in  datosConvert:
                    print(colored('As..................:','blue',attrs=['bold']),colored(datosConvert['as'],'yellow',attrs=['bold']))

                print(colored('URL site Maps.......:','blue',attrs=['bold']),colored('http://www.google.com/maps/place/' + str(datosConvert['lat']) + ',' + str(datosConvert['lon']) + '/@' + str(datosConvert['lat']) + ',' + str(datosConvert['lon']) + ',17z','yellow',attrs=['bold']))
                url='http://www.google.com/maps/place/' + str(datosConvert['lat']) + ',' + str(datosConvert['lon']) + '/@' + str(datosConvert['lat']) + ',' + str(datosConvert['lon']) + ',17z'

                print('                                                              ')
                opcionURL=input(colored('Quiere ver la URL de Google Maps en el navegador de firefox? ,Si=S o No=N ','blue',attrs=['bold']))

                if opcionURL.upper()=='S':
                    print(colored('El navegador utilizado por defecto es firefox','blue',attrs=['bold']))
                    navegador = "firefox"
                    abrirUrl(url,navegador)
        else:
            print(colored('[-] No se ha podido geolocalizar el objetivo, ' + 'Estado: ' + datosConvert['status'] ,'red',attrs=['bold']))
    else:
        print(colored('[-] No se ha podido geolocalizar el objetivo, ' + 'Respuesta: ' + respuesta.code ,'red',attrs=['bold']))
