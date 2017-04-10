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
REQUIREMENTS = ['openikeatradfri==0.1']

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_API_KEY): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the IKEA Tradfri Light platform."""

    import openikeatradfri

    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config.get(CONF_HOST)
    securitycode = config.get(CONF_API_KEY)

    api = openikeatradfri.api_factory(host, securitycode)
    hub = openikeatradfri.Hub(api)
    _LOGGER.debug("IKEA Tradfri Hub | init | Initialization Process Complete")

    lights = hub.get_lights()
    add_devices(IKEATradfri(light) for light in lights)

    _LOGGER.debug("IKEA Tradfri Hub | get_lights | All Lights Loaded")


class IKEATradfri(Light):
    """ The platform class required by hass """

    def __init__(self, light):
        """Initialize an IKEA Tradfri Light."""
        self._light = light
        self._name = light.name
        self._state = None #light.lights.is_on
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
