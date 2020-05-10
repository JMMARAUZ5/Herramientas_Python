#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#                            ANALIZANDO LOS METADATOS                             #
#  SE OBTIENEN LOS METADATOS DE DOCUMENTOS WORD QUE SE ENCUENTREN EN LA CARPETA    #
#  DESTINO.OBTENDREMOS TODOS LOS VALORES POSIBLES                                 #
###################################################################################

#Importamos los métodos que vamos a utilizar de la librería
from docx import Document
import os.path
from termcolor import colored

#Definimos una funcion que compruebe que el documento word esta en el directorio
#de no encontrar el documento word devuelve un error
def validar_word(docuword):
    name_dir = os.path.join(os.path.dirname(__file__),'Docu_WORDs')

    name_file = os.path.join(name_dir,docuword)

    if not os.path.isfile(name_file):
        print(colored("!!!!!!ERROR¡¡¡¡¡¡",'red',attrs=['bold']))
        print(colored("[+] No existe el fichero indicado,por favor revise nombre fichero,nombre debe de escribirse sin extension",'red',attrs=['bold']))
        print(colored("[+] Asegurese de tener el documento word en el directorio Docu_WORDs",'red',attrs=['bold']))
        print(colored("[+] Respete mayusculas y minusculas",'red',attrs=['bold']))
        return None
    else:
        return name_file

#Definimos una funcion que lea los datos del documento pdf en concreto
def analisis_docuword(name_file):

    try:
        #Leemos el archivo
        archivo_word =Document(name_file)
        #Obtenemos la información que queremos
        info_documento = archivo_word.core_properties
        return info_documento
    except:
        return None

def obtenermetaWORD():
    docuword=input(colored("Por favor, introduzca nombre del documento word indicando extension(.doc o .docx) a analizar,asegurese de que esta en el directorio Docu_WORDs: ",'green',attrs=['bold']))

    fileName=validar_word(docuword)

    if fileName != None:
        infoWord=analisis_docuword(fileName)
        return infoWord
    else:
        return None
