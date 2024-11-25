""" Switch Entity Related Classes """

import logging
from typing import Any
from dataclasses import dataclass

from homeassistant.core import callback
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# from .hub import Hub
from .api import ApiClient, Route, Listener

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

@dataclass
class SwitchConfiguration():
    """ Holds configutation to initalise a switch """
    def __init__(
        self,
        name: str,
        command: SwitchCommand,
        listener: Listener,
        invert: bool = False
    ) -> None:
        self.name: str = name
        self.command: SwitchCommand = command
        self.listener: Listener = listener
        self.invert: bool = invert


class Switch(SwitchEntity, CoordinatorEntity):
    """ Switch entity class """
    def __init__(self, configuration: SwitchConfiguration):

        self.configuration: SwitchConfiguration = configuration

        self._attr_name = self.configuration.name
        self._attr_unique_id = self._attr_name.lower().replace(" ", "_")
        # entity_description
        # _attr_device_class
        # _attr_state
        self.invert: bool = self.configuration.invert

        SwitchEntity.__init__(self)

        CoordinatorEntity.__init__(self, self.configuration.listener.coordinator)

    async def async_turn_on(self, **kwargs):
        """ Turns the switch on """
        _LOGGER.info("Command On")
        self._attr_is_on = not self.invert
        self.schedule_update_ha_state()
        self._attr_is_on = await self.configuration.command.set_position(self._attr_is_on)
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """ Turns the switch off """
        _LOGGER.info("Command Off")
        self._attr_is_on = self.invert
        self.schedule_update_ha_state()
        self._attr_is_on = await self.configuration.command.set_position(self._attr_is_on)
        self.schedule_update_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        is_on = self.configuration.listener.parse_response(self.coordinator.data)
        _LOGGER.debug("Coordinator Update: %s", self._attr_is_on)

        if (is_on != self._attr_is_on):
            self._attr_is_on = not is_on if self.invert else is_on
            _LOGGER.info("Coordinator Update Change: %s", self._attr_is_on)
            self.schedule_update_ha_state()


    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        raise NotImplementedError

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        raise NotImplementedError