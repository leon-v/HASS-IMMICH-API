"""Base class for all endpoints"""

import logging
from datetime import timedelta
from aiohttp.client import _RequestOptions
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from .switch import SwitchConfiguration
from .hub import Hub, Route
from .api import ValuePath

_LOGGER = logging.getLogger(__name__)

class Request:
    """ Sends a single HTTP request """
    def __init__(self, hub: Hub, route: Route, request_options: _RequestOptions) -> None:
        self.hub: Hub = hub
        self.route: Route = route
        self.request_options: _RequestOptions = request_options

    async def api_request(self):
        """ Send an API request to the configured route """
        return await self.hub.api_request(self.route, self.request_options)

class Listener:
    """ Used to rute responses to callbacks  """
    def __init__(self, coordinator: DataUpdateCoordinator, value_path: ValuePath) -> None:
        self.coordinator: DataUpdateCoordinator = coordinator
        self.value_path: ValuePath = value_path

class PollingRequest(CoordinatorEntity, Request):
    """ Sends a HTTP request on an interval"""
    def __init__(self, hub: Hub, route: Route, interval: timedelta, request_options: _RequestOptions = None) -> None:
        Request.__init__(self, hub, route, request_options)

        # TODO give this entity a name

        self.coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
            self.hub.hass,
            _LOGGER,
            name = f"{self.route.uri} Coordinator",
            update_method=self.coordinator_update,
            update_interval=interval,
        )

        super().__init__(self, self.coordinator)

    @callback
    async def coordinator_update(self):
        """ Performs the HTTP request when coordinator requests an update """
        return await self.api_request()



# May not need depednign on how jobs goes
class Endpoint:
    """ Base class for all endpoints """
    def __init__(self, hub: Hub) -> None:
        self.hub = hub
        self.switch_configurations: list[SwitchConfiguration] = []

    def add_switch_configutaion(self, switch_configuration: SwitchConfiguration):
        """ Adds a switch configuration to the queue """
        self.switch_configurations.append(switch_configuration)

    def get_switch_configurations(self) -> list[SwitchConfiguration]:
        return self.switch_configurations