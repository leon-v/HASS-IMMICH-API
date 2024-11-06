"""Platform for IMMICH Rest API sensor integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HubConfigEntry
from .Hub import Hub
from .QueueSizeNumberEntity import QueueSizeNumberEntity
from .QueueStatusBoolEntity import QueueStatusBoolEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add  sensors for passed config_entry in HA."""
    hub: Hub = config_entry.runtime_data

    async_add_entities(hub.getSensors())