#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        TRABAJANDO CON DNSPYTHON

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""""""""""""""
    CONSULTAS SOBRE VARIOS TIPOS DE REGISTRO
"""""""""""""""""""""""""""""""""""""""""""""""""""

import dns
import dns.resolver
from termcolor import colored
import pythonwhois               #Libreria para colores


def resolverDNS(dominio):
    try:
        """Consulta sobre registro IPV4"""
        ansA = dns.resolver.query(dominio,'A')

        #"""Consulta sobre registro IPV6"""
        #ansAAAA = dns.resolver.query(dominio,'AAAA')

        """Consulta sobre registro MailServers"""
        ansMX = dns.resolver.query(dominio,'MX')

        """Consulta sobre registro NameServers"""
        ansNS = dns.resolver.query(dominio,'NS')

        print (colored("Respuesta de DNS en IPV4: ",'blue',attrs=['bold', 'blink']))
        print (colored("==========================",'blue',attrs=['bold', 'blink']))
        #print (ansA.response.to_text())
        for i in ansA :
            print ("Nombres  de la IPs:  %s" % colored(i,'green',attrs=['bold']))
        #print (colored("\nRespuesta de DNS en IPV6: ",'red', attrs=['bold', 'blink']))
        #print (ansAAAA.response.to_text())

        print (colored("\nRespuesta de DNS en MailServers: ",'blue',attrs=['bold', 'blink']))
        print (colored("=================================",'blue',attrs=['bold', 'blink']))
        for i in ansMX :
            print ("Nombres  de los Mailservers:  %s" % colored(i,'green',attrs=['bold']))

        print (colored("\nRespuesta de DNS en NameServers: ",'blue',attrs=['bold', 'blink']))
        print (colored("================================",'blue',attrs=['bold', 'blink']))
        for i in ansNS :
            print ("Nombres  de los Servers:  %s" % colored(i,'green',attrs=['bold']))


        datos=pythonwhois.get_whois(dominio)

        print (colored("\nDatos obtenidos de  whois: ",'blue',attrs=['bold', 'blink']))
        print (colored("================================",'blue',attrs=['bold', 'blink']))
        if "contacts" in datos:
            print ("Contactos:"        )
            print ("   Admin:         %s" % colored(str(datos ['contacts']['admin']),'green',attrs=['bold']))
            print ("   Tech:          %s" % colored(str(datos ['contacts']['tech']),'green',attrs=['bold']))
            print ("   Registrant:    %s" % colored(str(datos ['contacts']['registrant']),'green',attrs=['bold']))
            print ("   Billing:       %s" % colored(str(datos ['contacts']['billing']),'green',attrs=['bold']))
        if "id" in datos:
            print ("Id:               %s" % colored(str(datos ['id'][0]),'green',attrs=['bold']))
        if "emails" in datos:
            print ("Emails:           %s" % colored(str(datos ['emails']),'green',attrs=['bold']))
        if "whois server" in datos:
            print ("Whois server:     %s" % colored(str(datos ['whois_server'][0]),'green',attrs=['bold']))
        if 'creation_date' in datos:
            print ("Fecha creacion:   %s" % colored(str(datos['creation_date'][0]),'green',attrs=['bold']))
        if 'expiration_date' in datos:
            print ("Fecha expiracion: %s" % colored(str(datos ['expiration_date'][0]),'green',attrs=['bold']))
        if 'registrar' in datos:
            print ("Registrar:        %s" % colored(str(datos ['registrar'][0]),'green',attrs=['bold']))
        if 'status' in datos:
            print ("Status:           %s" % colored(str(datos ['status'][0]),'green',attrs=['bold']))

    except dns.resolver.NoAnswer as e:
        print(colored("[-]Se ha producido un error Answer %s" % e ,'red',attrs=['bold']))
    except dns.resolver.NXDOMAIN as e:
        print(colored("[-]Se ha producido un error NXDomain  %s" % e ,'red',attrs=['bold']))
    except dns.resolver.YXDOMAIN as e:
        print(colored("[-]Se ha producido un error YXDomain  %s" % e ,'red',attrs=['bold']))
    except dns.resolver.NoNameservers as e:
        print(colored("[-]Se ha producido un error Domain  %s" % e ,'red',attrs=['bold']))
    except dns.resolver.Timeout as e:
        print(colored("[-]Se ha producido un error de Timeout  %s" % e ,'red',attrs=['bold']))
    except :
        print(colored("[-]Se ha producido un error inexperado" ,'red',attrs=['bold']))                                                                                                                                                                                                                                                                                                #    print(colored("[-]Lo sentimos error inesperado" ,'red',attrs=['bold']))
        exit()
