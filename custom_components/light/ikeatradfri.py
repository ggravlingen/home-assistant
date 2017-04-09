##############################################################
#
# IKEA TRADFRI LIGHT PLATFORM
# Version 0.1
#
#
#
##############################################################


import logging
import voluptuous as vol


# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, Light, PLATFORM_SCHEMA
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

    _LOGGER.debug("1")
    import ikea_v3
    
    _LOGGER.debug("2")
    # Assign configuration variables. The configuration check takes care they are
    # present. 
    _LOGGER.debug("3")
    host         = config.get(CONF_HOST)
    _LOGGER.debug("4")
    securitycode = config.get(CONF_PASSWORD)
    _LOGGER.debug("5")
    
    lights = []
    _LOGGER.debug("6")
    light = IKEATradfriHelper(host, securitycode, "65537")
    _LOGGER.debug("7")
    
    lights.append( light )
            
    # Add devices
    #add_devices( IKEATradfri(light) for light in lights )
    #add_devices( [ IKEATradfri(light) ] )
    _LOGGER.debug("8")
    add_devices( [ IKEATradfri( lights[0] ) ] )
    _LOGGER.debug("9")
    #add_devices( [ IKEATradfri( lights[0] ) ] )  # for light in lights )

class IKEATradfri(Light):
    """Representation of an Awesome Light."""
    
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