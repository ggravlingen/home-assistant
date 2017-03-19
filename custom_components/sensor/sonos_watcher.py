""" Just a different way of displaying current state of Sonos players  """
import logging
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from soco import SoCo

DEPENDENCIES = []

# Setup the logger platform
_LOGGER = logging.getLogger(__name__)

#SoCoData = SoCo(IP)

def setup_platform(hass, config, add_devices, discovery_info=None):
  """Setup the sensor platform."""

#  SoCoData = SoCo(IP)

  add_devices( [ SonosWatcher() ] )

class SonosWatcher(Entity):
  """Representation of a Sensor."""

  def __init__(self):
    _LOGGER.info("Sonos Data: initializing")

    ### Debug variables
    IP = "192.168.0.85"

    ### Get data from the SoCo Library
    loadSocoData = SoCo(IP)

    self._SoCoData = loadSocoData
    self._model_name = loadSocoData.get_speaker_info()['model_name']
    self._player_name = loadSocoData.player_name

    ### Misc
    self._icon = None
    self._state = loadSocoData.get_current_transport_info()['current_transport_state']

  @property
  def name(self):
    """Return the name of the sensor."""
    returnName = self._player_name + ' (mini)'
    return returnName

  @property
  def state(self):
    """Return the state of the sensor."""
    return self._state

  @property
  def entity_picture(self):
    """Type of player."""

    if self._model_name == "Sonos CONNECT":
      model_image = "http://demandware.edgesuite.net/sits_pod40/dw/image/v2/ABCG_PRD/on/demandware.static/-/Sites-sonos-master/default/dw00cb461e/images/connect/connect-front.png?sw=40&sh=40"

    return model_image


  def update(self):
    """Fetch new state data for the sensor.
    This is the only method that should fetch new data for Home Assistant.
    """
    SoCoData = self._SoCoData
    internalState = SoCoData.get_current_transport_info()['current_transport_state']
    if internalState == "PLAYING":
      self._state = "mdi:self.model_state_icon"
#      self._icon = "mdi:self.model_state_icon"
    else:
      self._state = "mdi:pause-octagon-outline"
#      self._icon = "mdi:pause-octagon-outline"
