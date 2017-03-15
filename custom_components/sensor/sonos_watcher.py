""" Just a different way of displaying current state of Sonos players  """

# https://github.com/Amir974/home-assistant-custom-components/blob/master/custom_components/notify/pushoverglances.py

import logging
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
import json, sys, urllib

#from homeassistant.const import (CONF_MONITORED_CONDITIONS, CONF_NAME)

DEPENDENCIES = []

CONF_START_IMAGE = 'startimage'
CONF_PLAY = 'playimage'
CONF_PAUSE = 'pauseimage'


DEFAULT_IMAGE = "http://demandware.edgesuite.net/sits_pod40/dw/image/v2/ABCG_PRD/on/demandware.static/-/Sites-sonos-master/default/dw00cb461e/images/connect/connect-front.png?sw=40&sh=40"
DEFAULT_PLAY = "https://image.flaticon.com/icons/svg/0/375.svg"
DEFAULT_PAUSE = "https://image.flaticon.com/icons/svg/61/61039.svg"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_START_IMAGE, default=DEFAULT_IMAGE): cv.string,
    vol.Optional(CONF_PLAY, default=DEFAULT_PLAY): cv.string,
    vol.Optional(CONF_PAUSE, default=DEFAULT_PAUSE): cv.string,
})

# Setup the logger platform
_LOGGER = logging.getLogger(__name__)



def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    picture = config.get(CONF_START_IMAGE)
#    name = config.get(DEFAULT_NAME)
#    devs = []
#    devs.append(SonosWatcher(name, force_update))
#    add_devices(devs)
    add_devices([ SonosWatcher(picture) ])


class SonosWatcher(Entity):
    """Representation of a Sensor."""

    def __init__(self, picture):
        """Initialize the sensor."""
        _LOGGER.info("Sonos Watcher: initializing")
        self._state = None
        self._picture = picture

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Sonos Vardagsrum (new)'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def entity_picture(self):
        """Type of player."""
        return self._picture
#sensor.sonos_kitchen_state

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
#        url_state = "http://192.168.0.140:5005/kitchen/state"
#        response_state = urllib.urlopen(url_playlist)
#        foo = json.load(response_state)["playbackState"]
#        _LOGGER.info(foo)
#        _LOGGER.info("asdasdasd")
#        _LOGGER.info(url_state)
        self._state = "Playing"
