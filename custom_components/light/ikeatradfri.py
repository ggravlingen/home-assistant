"""
Support for the IKEA Tradfri platform
Version 0.1
Thanks for the great support @balloob
"""

import logging


import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, \
    SUPPORT_BRIGHTNESS, Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_API_KEY
import homeassistant.helpers.config_validation as cv


SUPPORTED_FEATURES = (SUPPORT_BRIGHTNESS)

# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = ['opentradfri>=0.3']

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_API_KEY): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the IKEA Tradfri Light platform."""
    import opentradfri

    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config.get(CONF_HOST)
    securitycode = config.get(CONF_API_KEY)

    api = opentradfri.coap_cli.api_factory(host, securitycode)

    gateway = opentradfri.gateway.Gateway(api)
    devices = gateway.get_devices()
    lights = [dev for dev in devices if dev.has_light_control]

    _LOGGER.debug("IKEA Tradfri Hub | init | Initialization Process Complete")

    add_devices(IKEATradfri(light) for light in lights)
    _LOGGER.debug("IKEA Tradfri Hub | get_lights | All Lights Loaded")

class IKEATradfri(Light):
    """ The platform class required by hass """

    def __init__(self, light):
        """Initialize a Light."""
        self._light = light
        self._name = light.name
        self._state = None
        self._brightness = None

    @property
    def name(self): # working
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self): # working
        """Return true if light is on."""
        return self._light.light_control.lights[0].state

    @property
    def brightness(self): # working
        """Brightness of the light (an integer in the range 1-255).
        """
        return self._light.light_control.lights[0].dimmer

    def turn_off(self, **kwargs): # working
        """Instruct the light to turn off."""
        return self._light.light_control.set_dimmer(0)

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORTED_FEATURES

    def turn_on(self, **kwargs): # not working
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._light.brightness = kwargs.get(ATTR_BRIGHTNESS, 255) # not working
        self._light.light_control.set_dimmer(100)

    def update(self): # not working
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._light.update()
        #self._state = self._light.is_on()
        self._brightness = self._light.light_control.lights[0].dimmer
