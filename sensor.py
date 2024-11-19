"""Platform for IMMICH Rest API sensor integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .hub import Hub
from . import HubConfigEntry

async def async_setup_entry(
    hass: HomeAssistant,
    hub_config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add  sensors for passed hub_config_entry in HA."""
    hub: Hub = hub_config_entry.runtime_data

# Loop though switch config intances while creating the entities

    async_add_entities(hub.getSensors())


class SensorConfiguration():
    """Holds all the configuration required to fully configure a single sensor entity"""
    def __init__(self, hub: Hub):
        self.hub: Hub = hub
        pass