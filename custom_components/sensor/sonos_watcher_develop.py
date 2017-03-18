#!/usr/bin/python
# -*- coding: utf-8 -*-
#http://docs.python-soco.com/en/v0.11/index.html

import json, sys, urllib
import xml.etree.ElementTree as ET
from soco import SoCo


my_zone = SoCo('192.168.0.85')

foo = my_zone.get_speaker_info()['model_name']

print(foo)

class SonosWatcher:


#class SonosWatcher

"""
playerData = urllib.urlopen("http://192.168.0.85:1400/status/zp").read()

root = ET.fromstring(playerData)
#print root[0][19].tag

for item in root.findall('ZPInfo'):
  playerType = item.find('ExtraInfo').text


if "zp90" in playerType:
  sonosPlayerType = "Sonos Connect"
else:
  sonosPlayerType = "Unknown"


print sonosPlayerType
"""
