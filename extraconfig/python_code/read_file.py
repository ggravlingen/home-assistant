import sys

#Temperature:18.1
#Moisture:32
#Light:329
#Fertility:117

sensor = str(sys.argv[1])
variable = str(sys.argv[2])

filename = "/home/hass/.homeassistant/extraconfig/python_code/flowerdata/" + sensor + ".txt"

for line in open(filename):
  if variable in line:
    s_split = line.split(':')
    print s_split[1].rstrip("\n\r")

