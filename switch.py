"""Initalisation of all switch entities from all hubs"""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .hub import Hub
from . import HubConfigEntry
from homeassistant.components.switch import SwitchEntity

from .endpoint import Endpoint

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    hub_config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add  sensors for passed hub_config_entry in HA."""
    hub: Hub = hub_config_entry.runtime_data

    _LOGGER.debug(
        "hub.endpoints %s",
        hub.endpoints
    )

    endpoint: Endpoint
    switches: list[SwitchEntity] = []

    for endpoint in hub.endpoints:
        switches.extend(endpoint.get_switches())

    async_add_entities(switches)
