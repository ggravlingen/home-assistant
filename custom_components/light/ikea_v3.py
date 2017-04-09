# -*- coding: utf-8 -*-
# Version 1.0


#https://github.com/home-assistant/home-assistant/blob/5d5547cdb6dd91924e719c0b5e61e2b89e48e14b/homeassistant/components/light/yeelightsunflower.py
#https://github.com/lindsaymarkward/python-yeelight-sunflower/blob/master/yeelightsunflower/main.py#L80

import json, subprocess
import logging
_LOGGER = logging.getLogger(__name__)

def command_helper_v2(host, security_code, method, light_id = ''):
    """ Execute the command through shell """

#    _LOGGER.error(host + ' | ' + security_code + ' | ' + method + ' | ' + light_id)

    if len(light_id) > 0:
        commandString = 'coaps://' + host + ':5684/15001/' + light_id
    else:
        commandString = 'coaps://' + host + ':5684/15001'

    theCommand = [
        '/usr/local/bin/coap-client',
        '-u',
        'Client_identity',
        '-k',
        security_code,
        '-v',
        '0',
        '-m',
        method,
        commandString,
#        .'-f -'
        ]

    try:
        return_value = subprocess.check_output(theCommand)
        out = return_value.strip().decode('utf-8')
    except subprocess.CalledProcessError:
        _LOGGER.error('Command failed: %s', theCommand)

    """ Return only the last line, where there's JSON """
    output = json.loads(out.split('\n')[-1])

    return output


class IKEATradfriHub(object):
    """ This class connects to the IKEA Tradfri Gateway """

    def __init__(self, host, securityCode):
        self._bulbs = []

        self._host = host
        self._security_code = securityCode

        _LOGGER.debug("IKEA Tradfri Hub | init | Initialization Process Complete")

    def get_lights(self):
        """ Returns the lights linked to the gateway """
        output = command_helper_v2(self._host, self._security_code, 'get', '')

        for light_id in output:
            self._bulbs.append(IKEATradfriHelper(self._host,
                                                 self._security_code, light_id))

        _LOGGER.debug("IKEA Tradfri Hub | get_lights | All Lights Loaded")

        # return a list of Bulb objects
        return self._bulbs


class IKEATradfriHelper(object):
    """ Gets information on a specific device """

    def __init__(self, host, securityCode, light_id):
        self._devices = {}
        
        if light_id is not None:
            self._light_id = str(light_id)
        else:
            self._light_id = 0

        self._host = host
        self._security_code = securityCode

        self._name = None
        self._state = True
        self._brightness = None

    @property
    def name(self):
        """ Get the name of a device  """
        output = command_helper_v2(self._host, self._security_code, 'get', self._light_id)

        try:
            self._name = output['9001']
        except ValueError:
            _LOGGER.debug("IKEA Tradfri Helper | Name | Error Setting Name")

        return self._name

    @property
    def brightness(self):
        """ Get the brightness level """
        output = command_helper_v2(self._host, self._security_code, 'get', self._light_id)
        
        try:
            self._brightness = int(output['3311'][0]['5851'])+1 # The bulbs run from 0=off to 254=max but ha is 1-255
        except KeyError:
            _LOGGER.debug("IKEA Tradfri Helper | Brightness | KeyError")
        except TypeError:
            _LOGGER.debug("IKEA Tradfri Helper | Brightness | TypeError")

        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""

        if self._brightness is not None and self._brightness > 1:
            self._state = True
        else:
            self._state = False

        return self._state

#    def update(self):
#        """ Updates the state of the lamp """
#        self._state = this.is_on
#        self._brightness = this.brightness
