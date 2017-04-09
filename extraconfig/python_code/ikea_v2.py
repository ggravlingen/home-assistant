# -*- coding: utf-8 -*-
# Version 1.0

import os, sys, json,subprocess, array

"""
debug stuff
<//15001>;ct=0;obs,
	<//15001/65538>;ct=0;obs,
	<//15001/65536>;ct=0;obs,
	<//15001/65537>;ct=0;obs,
<//15001/reset>;ct=0,
	
<//15005>;ct=0;obs,
	<//15005/167992>;ct=0;obs,
	<//15005/167992/207144>;ct=0;obs,
	<//15005/167992/212063>;ct=0;obs,
	<//15005/167992/227453>;ct=0;obs,

<//status>;ct=0;obs,
<//15004/167992>;ct=0;obs,
<//15004>;ct=0;obs,
<//15004/add>;ct=0,
<//15004/remove>;ct=0,
<//15006>;ct=0;obs,
<//15011/15012>;ct=0;obs,
<//15011/9034>;ct=0,
<//15011/9030>;ct=0,
<//15011/9031>;ct=0,
<//15011/9063>;ct=0,
<//15011/9033>;ct=0,

<//15010>;ct=0;obs

{
	u'9019': 1,
	u'3':
		{
			u'1': u'TRADFRI bulb E27 WS opal 980lm',
			u'0': u'IKEA of Sweden',
			u'3': u'1.1.1.1-5.7.2.0',
			u'2': u'',
			u'6': 1},
	u'5750': 2,
	u'9003': 65537,
	u'9002': 1490985114,
	u'9001': u'K\xf6kslampa',
	u'3311': [
		{
			u'5708': 0,
			u'5709': 30140,
			u'5706': u'f1e0b5',
			u'5707': 0,
			u'5711': 0,
			u'5710': 26909,
			u'9003': 0,
			u'5851': 1,
			u'5850': 1
		}
			],
	u'9054': 0,
	u'9020': 1491664105}
	
	echo '{ "3311" : { "5851": 100 } }'                                     | coap-client -u 'Client_identity' -k 'PnHhjOjepj8vhbZB' -v 0 -m put 'coaps://192.168.0.129:5684/15001/65537'
	echo '{ "3311" : [{ "5851" : 100 , "5709": 33135 , "5710": 27211 } ] }' | coap-client -u "Client_identity" -k PnHhjOjepj8vhbZB -m put "coaps://192.168.0.129:5684/15001/65537" -f -
    echo '{ "3311" : { "5851": 1 } }'                                       | coap-client -u 'Client_identity' -k 'PnHhjOjepj8vhbZB' -v 0 -m put 'coaps://192.168.0.129:5684/15001/65537' -f -

"""

class IKEATradfriHelper(host, securitycode):

    #securityCode = "PnHhjOjepj8vhbZB"
    coapString = "coap-client -u 'Client_identity' -k '" + securityCode + "' -v 0 -m %s 'coaps://" + host + ":5684/%s' %s"

    def __init__(self):
	    self._devices = {}
		
    def setBrightness(self, deviceID, lightIntensity):
        commandString = "echo '{ \"3311\" : [{ \"5851\" : " + str(lightIntensity) + " }] }' | " + IKEATradfriHelper.coapString % ('put', "15001/" + deviceID , '-f -')
        proc = subprocess.Popen( commandString , stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

    def listDevices(self):
        proc = subprocess.Popen(IKEATradfriHelper.coapString % ("get", 15001, ""), stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        jsonStart = out.find("[", out.find("[") + 1 )
        output = json.loads( out[jsonStart:] )

        x = 0
        for device in output:
            self._devices[x] = self.deviceInfo(device)
            x = x + 1

    def deviceInfo(self, deviceID):
        command = IKEATradfriHelper.coapString % ("get", "15001/" + str(deviceID), "")
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


test = IKEATradfriHelper("192.168.0.129", "PnHhjOjepj8vhbZB")
test.listDevices()
test.setBrightness("65537", 180)
#print test._devices