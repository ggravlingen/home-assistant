"""
Support for the IKEA Tradfri platform
Version 0.1
Thanks for the great support @balloob
"""


import subprocess
import json
import logging
import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, \
    Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_API_KEY

import homeassistant.helpers.config_validation as cv


# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = []

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_API_KEY): cv.string,
})


def command_helper_v2(host, security_code, method, light_id = ''):
    """ Execute the command through shell """

    #_LOGGER.debug(host + ' | ' + security_code + ' | ' + method + ' | ' + light_id)

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
        commandString
        ]

    try:
        return_value = subprocess.check_output(theCommand)
        out = return_value.strip().decode('utf-8')
    except subprocess.CalledProcessError:
        _LOGGER.debug('Command failed: %s', theCommand)

    """ Return only the last line, where there's JSON """
    output = json.loads(out.split('\n')[-1])

    return output


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the IKEA Tradfri Light platform."""

    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config.get(CONF_HOST)
    securitycode = config.get(CONF_API_KEY)

    hub = IKEATradfriHub(host, securitycode)

    lights = hub.get_lights()
    add_devices(IKEATradfri(light) for light in lights)


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
        
        self._light_id = str(light_id)

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
        _LOGGER.debug( output['3311'][0]['5851'] )
        _LOGGER.debug( output['3311']['0']['5851'] )
        _LOGGER.debug(int(output['3311'][0]['5851']))

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

        if self._brightness > 1:
            self._state = True
        else:
            self._state = False

        return self._state

    def update(self):
        """ Updates the state of the lamp """
        self._state = this.is_on
        self._brightness = this.brightness

class IKEATradfri(Light):
    """ The platform class required by hass """

    def __init__(self, light):
        """Initialize an AwesomeLight."""
        self._light = light
        self._name = light.name
        self._state = None
        self._brightness = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Brightness of the light (an integer in the range 1-255).
        """
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._light.brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._light.turn_on()

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._light.turn_off()

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._light.update()
        self._state = self._light.is_on()
        self._brightness = self._light.brightness
