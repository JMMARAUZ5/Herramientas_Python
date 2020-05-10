#/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#                            ANALIZANDO LOS METADATOS                             #
#  SE OBTIENEN LOS METADATOS DE DOCUMENTOS excell QUE SE ENCUENTREN EN LA CARPETA #
#  DESTINO.OBTENDREMOS TODOS LOS VALORES POSIBLES                                 #
###################################################################################

#Importamos los métodos que vamos a utilizar de la librería
from openpyxl import load_workbook
import os.path
from termcolor import colored

#Definimos una funcion que compruebe que el documento  esta en el directorio
#de no encontrar el documento excell devuelve un error
def validar_excell(docuexcell):
    name_dir = os.path.join(os.path.dirname(__file__),'Docu_EXCELLs')

    name_file = os.path.join(name_dir,docuexcell)

    if not os.path.isfile(name_file):
        print(colored("!!!!!!ERROR¡¡¡¡¡¡",'red',attrs=['bold']))
        print(colored("[+] No existe el fichero indicado,por favor revise nombre fichero,nombre debe de escribirse con extension",'red',attrs=['bold']))
        print(colored("[+] Asegurese de tener el documento excell en el directorio Docu_EXCELLs",'red',attrs=['bold']))
        print(colored("[+] Respete mayusculas y minusculas",'red',attrs=['bold']))
        return None
    else:
        return name_file

#Definimos una funcion que lea los datos del documento pdf en concreto
def analisis_docuexcell(name_file):

    try:
        #Leemos el archivo
        archivo_excell =load_workbook(name_file)

        #Obtenemos la información que queremos
        info_documento = archivo_excell.properties

        return info_documento
    except:
        return None

def obtenermetaEXCELL():
    docuexcell=input(colored("Por favor, introduzca nombre del documento excell indicando extension(.xls o .xlsx) a analizar,asegurese de que esta en el directorio Docu_EXCELLs: ",'green',attrs=['bold']))

    fileName=validar_excell(docuexcell)
    if fileName != None:
        infoEXCELL=analisis_docuexcell(fileName)
        return infoEXCELL
    else:
        return None
