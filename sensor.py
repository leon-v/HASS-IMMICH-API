"""Platform for IMMICH Rest API sensor integration."""


import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity


from .hub import Hub
from . import HubConfigEntry

from .endpoint import Endpoint

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    hub_config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors to HA."""
    hub: Hub = hub_config_entry.runtime_data

    _LOGGER.debug(
        "hub.endpoints %s",
        hub.endpoints
    )

    endpoint: Endpoint
    sensors: list[SensorEntity] = []

    for endpoint in hub.endpoints:
        sensors.extend(endpoint.get_sensors())

    async_add_entities(sensors)

# class QueueStatus(TextEntity):
#     # Implement one of these methods.

#     def set_value(self, value: str) -> None:
#         """Set the text value."""

#     async def async_set_value(self, value: str) -> None:
#         """Set the text value."""
