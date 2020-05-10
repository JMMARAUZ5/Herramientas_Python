#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#                            ANALIZANDO LOS METADATOS                             #
#  SE OBTIENEN LOS METADATOS DE IMAGENES .JPG QUE SE ENCUENTREN EN LA CARPETA     #
#  DESTINO.OBTENDREMOS TODOS LOS VALORES POSIBLES                                 #
###################################################################################

#Importamos los métodos que vamos a utilizar de la librería
from PIL.ExifTags import TAGS,GPSTAGS
from PIL import Image
import os.path
from termcolor import colored

#Definimos una funcion que compruebe que la imagen esta en el directorio
#de no encontrar la imagen devuelve un error
def validar_imagen(imagen):
    name_dir = os.path.join(os.path.dirname(__file__),'Imagenes')

    name_file = os.path.join(name_dir,imagen)

    if not os.path.isfile(name_file):
        print(colored("!!!!!!ERROR¡¡¡¡¡¡",'red',attrs=['bold']))
        print(colored("[+] No existe el fichero indicado,por favor revise nombre fichero,nombre debe de escribirse sin extension",'red',attrs=['bold']))
        print(colored("[+] Asegurese de tener la imagen en el directorio Imagenes",'red',attrs=['bold']))
        print(colored("[+] Respete mayusculas y minusculas",'red',attrs=['bold']))
        return None
    else:
        return name_file

#Definimos una funcion que lea los datos de una imagen en concreto
def analisis_imagen(nombre_imagen):
    #Abrimos la imagen
    archivo_imagen = Image.open(nombre_imagen)

    #Extraemos la información necesaria de ella, los EXIF
    try:
        info = archivo_imagen._getexif()
        return info
    except:
        return None
    
def obtenermetaIMG():
    imagen=input(colored("Por favor, introduzca nombre de la imagen (sin extension) a analizar,asegurese de que esta en el directorio Imagenes: ",'green',attrs=['bold']))
    imagenExt=imagen + ".jpg"

    fileName=validar_imagen(imagenExt)

    if fileName != None:
        infoIMG=analisis_imagen(fileName)
        return infoIMG
    else:
        return None
