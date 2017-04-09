"""
Support for the IKEA Tradfri platform
Version 0.1
"""


import logging
import voluptuous as vol
import subprocess
import json

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, \
    Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_PASSWORD

import homeassistant.helpers.config_validation as cv


# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = []

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Awesome Light platform."""

    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config.get(CONF_HOST)
    securitycode = config.get(CONF_PASSWORD)

    hub = IKEATradfriHub(host, securitycode)

    _LOGGER.debug("IKEA Tradfri: 8")
    #hub.get_lights()
    add_devices(IKEATradfri(light) for light in hub.get_lights())
    _LOGGER.debug("IKEA Tradfri: 9")


class IKEATradfriHub(object):
    """ This class connects to the IKEA Tradfri Gateway """

    def __init__(self, host, securityCode):

        self._bulbs = []
        self._coap_string = "coap-client -u 'Client_identity' -k '" \
            + securityCode + "' -v 0 -m %s 'coaps://" + host + ":5684/%s' %s"

        self._host = host
        self._security_code = securityCode

        _LOGGER.debug("IKEA Tradfri Hub: Initialized")

    def get_lights(self):
        """ Returns the lights linked to the gateway """
        output = self.command_helper(self._coap_string, ("get", "15001", ""), "[")
        _LOGGER.debug("IKEA Tradfri Hub: Get Lights [1]")

        for light_id in output:
            self._bulbs.append(IKEATradfriHelper(self._host,
                                                 self._security_code, light_id))

        _LOGGER.debug("IKEA Tradfri Hub: Get Lights [2]")

        # return a list of Bulb objects
        return self._bulbs

    @staticmethod
    def command_helper(command, arguments, needle):
        """ Execute the command through shell """

        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [1]")

        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [2]")
        proc = subprocess.Popen(command % arguments, stdout=subprocess.PIPE, shell=True)
        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [3]")
        (out, err) = proc.communicate()
        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [4]")

        JSON_START = out.find(needle, out.find(needle) + 1)
        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [5]")
        output = json.loads(out[JSON_START:])
        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [6]")

        return output


class IKEATradfri(Light):
    """ The platform class required by hass """

    def __init__(self, light):
        """Initialize an AwesomeLight."""
        self._light = light
        self._name = light.name
        self._state = None
        self._brightness = None
        _LOGGER.info("IKEA Tradfri: test")

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Brightness of the light (an integer in the range 1-255).

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
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


class IKEATradfriHelper(object):
    """ Gets information on a specific device """

    def __init__(self, host, securityCode, device_id):
        self._devices = {}
        self._device_id = device_id
        self._coap_string = "coap-client -u 'Client_identity' -k '" \
            + securityCode + "' -v 0 -m %s 'coaps://" + host + ":5684/%s' %s"

        self._name = None
        self._state = True
        self._brightness = None

    @property
    def name(self):
        """ Get the name of a device  """
        output = self.command_helper(
            self._coap_string,
            ("get", "15001/" + str(self._device_id), ""),
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
        output = self.command_helper(
            self._coap_string,
            ("get", "15001/" + str(self._device_id), ""),
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

    @staticmethod
    def command_helper(command, arguments, needle):
        """ Execute the command through shell """

        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [1]")

        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [2]")
        proc = subprocess.Popen(command % arguments, stdout=subprocess.PIPE, shell=True)
        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [3]")
        (out, err) = proc.communicate()
        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [4]")

        JSON_START = out.find(needle, out.find(needle) + 1)
        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [5]")
        output = json.loads(out[JSON_START:])
        _LOGGER.debug("IKEA Tradfri Hub: Command Helper [6]")

        return output
