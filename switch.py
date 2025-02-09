"""Initalisation of all switch entities from all hubs"""

import logging
from typing import Any
from dataclasses import dataclass

from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import ApiClient, Route, Listener
from .hub import Hub
from . import HubConfigEntry
from .endpoint import Endpoint

_LOGGER = logging.getLogger(__name__)


@dataclass
class SwitchCommand():
    """ All parameters required to interact with a switch """
    def __init__(
        self,
        api_client: ApiClient,
        route: Route,
        on_data: object,
        off_data: object
    ) -> None:
        self.api_client: ApiClient = api_client
        self.route: Route = route
        self.on_data: object = on_data
        self.off_data: object = off_data

    async def set_position(self, position: bool):
        """ Sets the switch position """
        send_data = self.on_data if position else self.off_data
        return await self.api_client.send(self.route, json = send_data)


class Switch(SwitchEntity, CoordinatorEntity):

    """ Switch entity class """
    def __init__(
        self,
        name: str,
        command: SwitchCommand,
        listener: Listener,
        invert: bool = False
        #description: SwitchEntityDescription = None
    ):

        self.command: SwitchCommand = command
        self.listener: Listener = listener
        self._invert: bool = invert

        self._attr_name = name
        self._attr_unique_id = self._attr_name.lower().replace(" ", "_")
        #self.entity_description = description
        # _attr_device_class
        # _attr_state

        SwitchEntity.__init__(self)

        CoordinatorEntity.__init__(self, self.listener.coordinator)

    def invert(self, value: bool):
        """ Inverts the value if configured to do so """
        return (not value) if self._invert else value

    async def async_turn_on(self, **kwargs):
        """ Turns the switch on """
        await self.async_set_position(True, **kwargs)

    async def async_turn_off(self, **kwargs):
        """ Turns the switch off """
        await self.async_set_position(False, **kwargs)

    async def async_set_position(self, position: bool, **kwargs):
        """ Turns the switch on or off """

        self._attr_is_on = position
        self.schedule_update_ha_state()
        _LOGGER.info("[%s]Command Set: %s", self._attr_unique_id, self._attr_is_on)

        position = self.invert(self._attr_is_on)
        position = await self.command.set_position(position)
        self._attr_is_on = self.invert(position)
        self.schedule_update_ha_state()
        _LOGGER.info("[%s]Command Got: %s", self._attr_unique_id, self._attr_is_on)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        position = self.listener.parse_response_value(self.coordinator.data)
        position = self.invert(position)
        _LOGGER.debug("[%s]Coordinator Update: %s", self._attr_unique_id, position)

        if (position != self._attr_is_on):
            self._attr_is_on = position
            _LOGGER.info("[%s]Coordinator Update Change: %s", self._attr_unique_id, self._attr_is_on)
            self.schedule_update_ha_state()

        if (self.listener.attribute_path):
            self._attr_extra_state_attributes = self.listener.parse_response_attribute(self.coordinator.data)

        super()._handle_coordinator_update()


    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        raise NotImplementedError

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        raise NotImplementedError


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
