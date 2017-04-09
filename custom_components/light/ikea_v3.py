# -*- coding: utf-8 -*-
# Version 1.0

import json, subprocess

def commandHelper(command, arguments):
    proc = subprocess.Popen( command % arguments , stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    jsonStart = out.find("{", out.find("{") + 1 )
    output = json.loads( out[jsonStart:] )
    
    return output

class IKEATradfriHelper(object):

    def __init__(self, host, securityCode, deviceID):
        self._devices = {}
        self._deviceID = deviceID
        self._coapString = "coap-client -u 'Client_identity' -k '" + securityCode + "' -v 0 -m %s 'coaps://" + host + ":5684/%s' %s"
        
        self._name = None
        self._state = True
        self._brightness = None

    @property
    def name(self):
        output = commandHelper(self._coapString, ("get", "15001/" + str(self._deviceID), "") )
		
        try:
            self._name = output["9001"]
        except ValueError:
		    error = 1 # print("No device")
		
        return self._name
        
    @property
    def brightness(self):
        output = commandHelper(self._coapString, ("get", "15001/" + str(self._deviceID), "") )
        
        try:
            self._brightness = int(output["3311"][0]["5851"])
        except KeyError:
		    error = 1 # print("No device")
        except TypeError:
		    error = 1 # print("No device")
		
        return self._brightness
        
    @property
    def is_on(self):
        """Return true if light is on."""
        
        if self._brightness > 0:
            self._state = True
        else:
            self._state = False
            
        return self._state
        
    ########### below is debug, ignore
"""
    def setBrightness(self, deviceID, lightIntensity):
        commandString = "echo '{ \"3311\" : [{ \"5851\" : " + str(lightIntensity) + " }] }' | " + self._coapString % ('put', "15001/" + deviceID , '-f -')
        proc = subprocess.Popen( commandString , stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

    def listDevices(self):
        proc = subprocess.Popen(self._coapString % ("get", 15001, ""), stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        jsonStart = out.find("[", out.find("[") + 1 )
        output = json.loads( out[jsonStart:] )

        x = 0
        for device in output:
            self._devices[x] = self.deviceInfo(device)
            x = x + 1
			
	

    def deviceInfo(self, deviceID):
        command = self._coapString % ("get", "15001/" + str(deviceID), "")
        proc = subprocess.Popen( command , stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        jsonStart = out.find("{", out.find("{") + 1 )
        output = json.loads( out[jsonStart:] )
		
        itemName       = None
        lightIntensity = None
        lightSetting   = None
        lightSettingA  = None
        lightSettingB  = None
		
        try:
            itemName = output["9001"]
        except ValueError:
		    error = 1 # print("No device")

        try:
            lightIntensity = output["3311"][0]["5851"]
        except KeyError:
		    error = 1 # print("No device")
        except TypeError:
		    error = 1 # print("No device")
			
        try:
            lightSettingA = output["3311"][0]["5709"]
        except KeyError:
		    error = 1 # print("No device")
        except TypeError:
		    error = 1 # print("No device")

        try:
            lightSettingB = output["3311"][0]["5710"]
        except KeyError:
		    error = 1 # print("No device")
        except TypeError:
		    error = 1 # print("No device")
		
        try:
            if lightSettingA == 24930 and lightSettingB == 24694:
                lightSetting = "4000K"
            elif lightSettingA == 30140 and lightSettingB == 26909:
                lightSetting = "2700K"
            elif lightSettingA == 33135 and lightSettingB == 27211:
                lightSetting = "2200K"
        except KeyError:
		    error = 1 # print("No device")
        except TypeError:
		    error = 1 # print("No device")
			
        itemInfo = [
            { 'ID'   : deviceID },
            { 'Name' : itemName },
            { 'Intensity' : lightIntensity },
            { 'Light Setting' : lightSetting },
		]
		
        return itemInfo

https://dev-docs.home-assistant.io/en/dev/api/homeassistant.html#module-homeassistant.const

#def setup(hass, config):
#    IKEA['light'] = []
#    IKEA['light'].append( IKEATradfriHelper( host, securitycode, "65537" ) )
    
class IKEATradfriHelperTop(object):
    def __init__(self, host, securitycode, deviceID):
        self._host         = host
        self._securitycode = securitycode
        self._deviceID     = deviceID
        self._lightList = []
        self._lights = []

    def lights(self):
        self._lights.append ( IKEATradfriHelper(self._host, self._securitycode, self._deviceID) )
        return self._lights         
 """