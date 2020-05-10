#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""

    OBTENER MAC DE EQUIPO

"""""""""""""""""""""""""""""""""""""""""""""""""""

import getmac
import sys
from scapy.all import *
from termcolor import colored

mimac=getmac.get_mac_address()

#packet = Ether()/ARP(op="who-has",hwsrc=my_mac,psrc=self.dstAddress,pdst=self.srcAddress)
#sendp(Ether()/ARP(op=2,hwsrc=mimac,psrc='192.168.189.254',pdst='192.168.189.167'))
#sendp(Ether()/ARP(op=2,hwsrc=mimac,psrc='192.168.189.167',pdst='192.168.189.254'))
print("Direccion MAC: " + str(mimac) )
