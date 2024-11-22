""" Switch Entity Related Classes """

import logging
from typing import Any
from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# from .hub import Hub
from .api import ApiClient, ValuePath, Route, Listener

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
        listener: Listener
    ) -> None:
        self.name: str = name
        self.command: SwitchCommand = command
        self.listener: Listener = listener


class Switch(SwitchEntity, CoordinatorEntity):
    """ Switch entity class """
    def __init__(self, configuration: SwitchConfiguration):

        self.configuration: SwitchConfiguration = configuration
        self._name: str = self.configuration.name

        SwitchEntity.__init__(self)
        CoordinatorEntity.__init__(self, self.configuration.listener.coordinator)

    async def async_turn_on(self, **kwargs):
        """ Turns the switch on """
        _LOGGER.debug("Command On")
        self._attr_is_on = True
        await self.configuration.command.set_position(self._attr_is_on)
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """ Turns the switch off """
        _LOGGER.debug("Command Off")
        self._attr_is_on = False
        await self.configuration.command.set_position(self._attr_is_on)
        self.schedule_update_ha_state()

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        raise NotImplementedError

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        raise NotImplementedError