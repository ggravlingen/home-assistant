#!/usr/bin/python

import sys
import time

from miflora.miflora_poller import MiFloraPoller, \
    MI_FERTILITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE



myArgument = str(sys.argv[1])


if myArgument == "nr1":
  myMAC = "C4:7C:8D:61:3C:D9"
elif myArgument == "nr2":
  myMAC = "C4:7C:8D:61:3C:DC"
else:
  myMAC = "C4:7C:8D:61:7E:CC"

poller = MiFloraPoller(myMAC)

f = open("/home/hass/.homeassistant/extraconfig/python_code/flowerdata/" + myArgument +".txt","w")

f.write(myArgument + "\n")
f.write(time.strftime("%Y-%m-%d %H:%M:%S")+ "\n")
f.write("Temperature:{}".format(poller.parameter_value("temperature")) + "\n")
f.write("Moisture:{}".format(poller.parameter_value(MI_MOISTURE)) + "\n")
f.write("Light:{}".format(poller.parameter_value(MI_LIGHT)) + "\n")
f.write("Fertility:{}".format(poller.parameter_value(MI_FERTILITY)) + "\n")

f.close()

