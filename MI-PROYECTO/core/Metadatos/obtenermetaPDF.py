#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#                            ANALIZANDO LOS METADATOS                             #
#  SE OBTIENEN LOS METADATOS DE DOCUMENTOS PDF QUE SE ENCUENTREN EN LA CARPETA    #
#  DESTINO.OBTENDREMOS TODOS LOS VALORES POSIBLES                                 #
###################################################################################

#Importamos los métodos que vamos a utilizar de la librería
from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
from termcolor import colored

#Definimos una funcion que compruebe que el documento pdf esta en el directorio
#de no encontrar el documento pdf devuelve un error
def validar_pdf(docupdfExt):
    name_dir = os.path.join(os.path.dirname(__file__),'Docu_PDFs')

    name_file = os.path.join(name_dir,docupdfExt)

    if not os.path.isfile(name_file):
        print(colored("!!!!!!ERROR¡¡¡¡¡¡",'red',attrs=['bold']))
        print(colored("[+] No existe el fichero indicado,por favor revise nombre fichero,nombre debe de escribirse sin extension",'red',attrs=['bold']))
        print(colored("[+] Asegurese de tener el documento pdf en el directorio Docu_PDFs",'red',attrs=['bold']))
        print(colored("[+] Respete mayusculas y minusculas",'red',attrs=['bold']))
        return None
    else:
        return name_file

#Definimos una funcion que lea los datos del documento pdf en concreto
def analisis_docupdf(name_file):

    try:
        #Leemos el archivo
        archivo_pdf = PdfFileReader(name_file,'rb')

        #Obtenemos la información que queremos
        info_documento = archivo_pdf.getDocumentInfo()
        return info_documento
    except:
        return None


def obtenermetaPDF():
    docupdf=input(colored("Por favor, introduzca nombre del documento pdf(sin extension) a analizar,asegurese de que esta en el directorio Docu_PDFs: ",'green',attrs=['bold']))
    docupdfExt=docupdf + ".pdf"

    fileName=validar_pdf(docupdfExt)
    if fileName != None:
        infoPDF=analisis_docupdf(fileName)
        return infoPDF
    else:
        return None
