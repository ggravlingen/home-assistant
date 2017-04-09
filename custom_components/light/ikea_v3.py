# -*- coding: utf-8 -*-
# Version 1.0


#https://github.com/home-assistant/home-assistant/blob/5d5547cdb6dd91924e719c0b5e61e2b89e48e14b/homeassistant/components/light/yeelightsunflower.py
#https://github.com/lindsaymarkward/python-yeelight-sunflower/blob/master/yeelightsunflower/main.py#L80

import json, subprocess
import logging
_LOGGER = logging.getLogger(__name__)

class IKEATradfriHub(object):
    """ This class connects to the IKEA Tradfri Gateway """
    
    import subprocess

    def __init__(self, host, securityCode):
        self._bulbs = []
        self._coapString = "coap-client -u 'Client_identity' -k '" \
            + securityCode + "' -v 0 -m %s 'coaps://" + host + ":5684/%s' %s"

        self._host = host
        self._securityCode = securityCode

        _LOGGER.debug("IKEA Tradfri Hub: Initialized")

    def get_lights(self):
        """ Returns the lights linked to the gateway """
        output = self.commandHelper(self._coapString, ("get", "15001", ""), "[")

        _LOGGER.debug("IKEA Tradfri Hub: Get Lights loaded")

        for light_id in output:
            self._bulbs.append(IKEATradfriHelper(self._host,
                                                 self._securityCode, light_id))

        # return a list of Bulb objects
        return self._bulbs

    def commandHelper(self, command, arguments, needle):
        """ Execute the command through shell """

        shellCommand = command % arguments
        proc = subprocess.Popen(shellCommand, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        jsonStart = out.find(needle, out.find(needle) + 1)
        output = json.loads(out[jsonStart:])

        return output

        
class IKEATradfriHelper(object):
    """ Gets information on a specific device """

    def __init__(self, host, securityCode, deviceID):
        self._devices = {}
        self._deviceID = deviceID
        self._coapString = "coap-client -u 'Client_identity' -k '" \
            + securityCode + "' -v 0 -m %s 'coaps://" + host + ":5684/%s' %s"

        self._name = None
        self._state = True
        self._brightness = None

    @property
    def name(self):
        """ Get the name of a device  """
        output = commandHelper(
            self._coapString,
            ("get", "15001/" + str(self._deviceID), ""),
            "{"
            )

        try:
            self._name = output["9001"]
        except ValueError:
            _LOGGER.debug("IKEA Tradfri Hub: Error getting name")

        return self._name

    @property
    def brightness(self):
        """ Get the brightness level """
        output = commandHelper(
            self._coapString,
            ("get", "15001/" + str(self._deviceID), ""),
            "{"
            )

        try:
            self._brightness = int(output["3311"][0]["5851"])
        except KeyError:
            _LOGGER.debug("IKEA Tradfri Hub: Error getting brightness")
        except TypeError:
            _LOGGER.debug("IKEA Tradfri Hub: Error getting brightness")

        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""

        if self._brightness > 0:
            self._state = True
        else:
            self._state = False

        return self._state
