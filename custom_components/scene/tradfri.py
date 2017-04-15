"""Support for IKEA Tradfri Moods."""
import logging

from homeassistant.components.scene import Scene
from homeassistant.components.tradfri import WinkDevice, DOMAIN


DEPENDENCIES = ['pytradfri']
_LOGGER = logging.getLogger(__name__)



def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Wink platform."""
    import pytradfri
    
    moods = pytradfri.gateway.get_moods()
    
    for scene in moods:
        _id = scene.id() + scene.name()
        if _id not in hass.data[DOMAIN]['unique_ids']:
            add_devices([TradfriMood(scene)])
            
    _LOGGER.debug("IKEA Tradfri Scene Platform | init | Platform setup complete")


class TradfriMood(TradfriDevice, Scene):
    """Representation of a Tradfri mood."""

    def __init__(self, scene):
        """Initialize the scene."""
        self._scene = scene
        self._index = scene.id
        self._name = scene.name

    @property
    def name(self):
        """Return the name of the scene."""
        return self._name
