#!/usr/bin/python
# -*- coding: utf-8 -*-
#http://docs.python-soco.com/en/v0.11/index.html

import json, sys, urllib
import xml.etree.ElementTree as ET
from soco import SoCo

class SonosWatcher(object):
  def __init__(self, IP):

    self.SoCoData = SoCo(IP)

    self.model_name = self.SoCoData.get_speaker_info()['model_name']
    self.player_name = self.SoCoData.player_name

    self.model_image = None
    self.model_state = None
    self.model_state_icon = None

    ### Set base state for the player
    self.setState()

    ### Set an image for the current player
    #self setImage()

  def setState(self):
    internalState = self.SoCoData.get_current_transport_info()['current_transport_state']
    if internalState == "PLAYING":
      self.model_state = "Playing"
      self.model_state_icon = "mdi:self.model_state_icon"
    else:
      self.model_state = "Paused"
      self.model_state_icon = "mdi:pause-octagon-outline"


  def setImage(self):
    if self.model_name == "Sonos CONNECT":
      self.model_image = "http://demandware.edgesuite.net/sits_pod40/dw/image/v2/ABCG_PRD/on/demandware.static/-/Sites-sonos-master/default/dw00cb461e/images/connect/connect-front.png?sw=40&sh=40"




test = SonosWatcher("192.168.0.85")
print(test.model_name)
print(test.player_name)
print(test.model_state)
