#/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#                            ANALIZANDO LOS METADATOS                             #
#  SE OBTIENEN LOS METADATOS DE DOCUMENTOS PPT QUE SE ENCUENTREN EN LA CARPETA    #
#  DESTINO.OBTENDREMOS TODOS LOS VALORES POSIBLES                                 #
###################################################################################

#Importamos los métodos que vamos a utilizar de la librería
from pptx import Presentation
import os.path
from termcolor import colored

#Definimos una funcion que compruebe que el documento  esta en el directorio
#de no encontrar el documento ppt devuelve un error
def validar_ppt(docuppt):
    name_dir = os.path.join(os.path.dirname(__file__),'Docu_PPTs')

    name_file = os.path.join(name_dir,docuppt)

    if not os.path.isfile(name_file):
        print(colored("!!!!!!ERROR¡¡¡¡¡¡",'red',attrs=['bold']))
        print(colored("[+] No existe el fichero indicado,por favor revise nombre fichero,nombre debe de escribirse con extension",'red',attrs=['bold']))
        print(colored("[+] Asegurese de tener el documento ppt en el directorio Docu_PPTs",'red',attrs=['bold']))
        print(colored("[+] Respete mayusculas y minusculas",'red',attrs=['bold']))
        return None
    else:
        return name_file

#Definimos una funcion que lea los datos del documento pdf en concreto
def analisis_docuppt(name_file):

    try:
        #Leemos el archivo
        archivo_ppt =Presentation(name_file)

        #Obtenemos la información que queremos
        info_documento = archivo_ppt.core_properties
        return info_documento
    except:
        return None


def obtenermetaPPT():
    docuppt=input(colored("Por favor, introduzca nombre del documento ppt indicando extension(.ppt o .pptx) a analizar,asegurese de que esta en el directorio Docu_PPTs: ",'green',attrs=['bold']))

    fileName=validar_ppt(docuppt)
    if fileName != None:
        infoPPT=analisis_docuppt(fileName)
        return infoPPT
    else:
        return None
