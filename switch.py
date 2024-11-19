"""Initalisation of all switch entities from all hubs"""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .hub import Hub
from . import HubConfigEntry
from .switch_entity import Switch

from .endpoint import Endpoint

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    hub_config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add  sensors for passed hub_config_entry in HA."""
    hub: Hub = hub_config_entry.runtime_data

    # Loop though switch config intances while creating the entities

    switches: list[Switch] = []
    endpoint: Endpoint
    for endpoint in hub.endpoints:
        for switch_configuration in endpoint.get_switch_configurations():
            switches.append(Switch(switch_configuration))

    async_add_entities(switches)
