"""Initalisation of all switch entities from all hubs"""

import logging
from dataclasses import dataclass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from . import HubConfigEntry
from .hub import Hub, Route
from .api import ValuePath
from .endpoint import Endpoint, Listener


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

@dataclass
class SwitchCommand():
    """ All parameters required to interact with a switch """
    def __init__(
        self,
        route: Route,
        on_data: ValuePath,
        off_data: ValuePath
    ) -> None:
        self.route: Route = route
        self.on_data: ValuePath = on_data
        self.off_data: ValuePath = off_data

@dataclass
class SwitchConfiguration():
    """ Hold configutation to initalise a switch """
    def __init__(
        self,
        name: str,
        command: SwitchCommand,
        listener: Listener
    ) -> None:
        self.name: str = name
        self.command: SwitchCommand = command
        self.listener: Listener = listener


class Switch(CoordinatorEntity):
    """ Switch entity class """
    def __init__(self, configuration: SwitchConfiguration):
        pass
