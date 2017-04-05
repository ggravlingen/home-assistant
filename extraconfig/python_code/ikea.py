# -*- coding: utf-8 -*-
# ikea.py
import os, sys

# Printed on the back of your gateway
#securityCode = "xxx"

from ikea_pw import *
# the file ikea_pw, stored in the same folder as this script, contains nothing but
# securityCode = "xxx"

### --- extract code from here

# The id number of your lamp
#lampID = "65537"
lampID = str(sys.argv[1])

# The light intensity [0=off, 255]
#lightIntensity = "180"
lightIntensity = str(sys.argv[2])

#lightSetting = "Yellow" # White | Middle | Yellow
lightSetting = str(sys.argv[3])

if lightSetting == "4000K":
  lightColorA = "24930"
  lightColorB = "24694"
elif lightSetting == "2700K":
  lightColorA = "30140"
  lightColorB = "26909"
else:
  lightColorA = "33135"
  lightColorB = "27211"


stringCommand = """echo '{ "3311" : [{ "5851" : """ + lightIntensity + """ , "5709": """ + lightColorA + """ , "5710": """ + lightColorB + """ } ] }'"""
stringCoap = """coap-client -u "Client_identity" -k """ + securityCode + """ -m put "coaps://192.168.0.129:5684/15001/""" + lampID + """" -f -"""

print(stringCommand + " | " + stringCoap)


os.system(stringCommand + " | " + stringCoap)
