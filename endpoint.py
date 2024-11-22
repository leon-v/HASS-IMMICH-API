"""Base class for all endpoints"""

import logging
from datetime import timedelta
from aiohttp.client import _RequestOptions

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

from .switch_entity import SwitchConfiguration
from .api import ApiClient
# from .hub import Hub
from .api import Route

_LOGGER = logging.getLogger(__name__)

class Request:
    """ Sends a single HTTP request """
    def __init__(self, api_client: ApiClient, route: Route, request_options: _RequestOptions) -> None:
        self.api_client: ApiClient = api_client
        self.route: Route = route
        self.request_options: _RequestOptions = request_options

class PollingRequest(CoordinatorEntity, Request):
    """ Sends a HTTP request on an interval"""
    def __init__(
            self,
            hass: HomeAssistant,
            api_client: ApiClient,
            route: Route,
            interval: timedelta,
            request_options: _RequestOptions = None
    ) -> None:

        self.hass: HomeAssistant = hass

        Request.__init__(self, api_client, route, request_options)

        # TODO give this entity a name

        self.coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
            self.hass,
            _LOGGER,
            name = f"{self.route.uri} Coordinator",
            update_method=self.coordinator_update,
            update_interval=interval,
        )

        super().__init__(self, self.coordinator)

    @callback
    async def coordinator_update(self):
        """ Performs the HTTP request when coordinator requests an update """
        return await self.api_client.send(self.route, self.request_options)



# May not need depednign on how jobs goes
class Endpoint:
    """ Base class for all endpoints """
    def __init__(
            self,
            hass: HomeAssistant,
            api_client: ApiClient
        ) -> None:
        self.hass: HomeAssistant = hass
        self.api_client: ApiClient = api_client

        self.switch_configurations: list[SwitchConfiguration] = []

    def add_switch_configutaion(self, switch_configuration: SwitchConfiguration):
        """ Adds a switch configuration to the queue """
        self.switch_configurations.append(switch_configuration)

    def get_switch_configurations(self) -> list[SwitchConfiguration]:
        """ Gets switch configurations """
        return self.switch_configurations