"""Base class for all endpoints"""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity


from .api import ApiClient
# from .hub import Hub
from .api import Route

_LOGGER = logging.getLogger(__name__)

class Request:
    """ Sends a single HTTP request """
    def __init__(self, api_client: ApiClient, route: Route, **request_arguments) -> None:
        self.api_client: ApiClient = api_client
        self.route: Route = route
        self.request_arguments = request_arguments

    async def send(self):
        """ Sends this request """
        return await self.api_client.send(self.route, **self.request_arguments)


class PollingRequest(CoordinatorEntity, Request):
    """ Sends a HTTP request on an interval"""
    def __init__(
            self,
            hass: HomeAssistant,
            api_client: ApiClient,
            name: str,
            route: Route,
            interval: timedelta,
            **request_arguments
    ) -> None:
        self.hass: HomeAssistant = hass

        self._attr_name = name
        self._attr_unique_id = self._attr_name.lower().replace(" ", "_")
        self._attr_icon = "mdi:api"

        Request.__init__(self, api_client, route, **request_arguments)

        self.coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
            self.hass,
            _LOGGER,
            name = f"{self.route.uri} Coordinator",
            update_method = self.coordinator_update,
            update_interval = interval,
        )

        CoordinatorEntity.__init__(self, self.coordinator)

    @callback
    async def coordinator_update(self):
        """ Performs the HTTP request when coordinator requests an update """

        result = await self.send()
        self._attr_state = 'OK'
        self._attr_extra_state_attributes = result
        return result

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

        self.switches: list[SwitchEntity] = []
        self.sensors: list[SensorEntity] = []

    def add_switch(self, switch: SwitchEntity) -> None:
        """ Adds a configured switch """
        self.switches.append(switch)

    def get_switches(self) -> list[SwitchEntity]:
        """ Creates or gets switches """
        return self.switches

    def add_sensor(self, sensor: SensorEntity) -> None:
        """ Adds a configured sensor """
        self.sensors.append(sensor)

    def get_sensors(self) -> list[SensorEntity]:
        """ Creates or gets sensors """
        return self.sensors

