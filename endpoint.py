"""Base class for all endpoints"""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity



from .switch_entity import SwitchConfiguration, Switch
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
        return await self.api_client.send(self.route, **self.request_arguments)


class PollingRequest(CoordinatorEntity, Request):
    """ Sends a HTTP request on an interval"""
    def __init__(
            self,
            hass: HomeAssistant,
            api_client: ApiClient,
            route: Route,
            interval: timedelta,
            **request_arguments
    ) -> None:

        self.hass: HomeAssistant = hass

        Request.__init__(self, api_client, route, **request_arguments)

        # TODO give this entity a name

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
        return await self.send()



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
        self.switches_initialised = False
        self.switch_configurations: list[SwitchConfiguration] = []

        self.sensors: list[SensorEntity] = []
        self.sensors_initialised = False
        self.sensor_configurations: list[SwitchConfiguration] = []

    def add_switch_configutaion(self, switch_configuration: SwitchConfiguration):
        """ Adds a switch configuration to the queue """
        self.switch_configurations.append(switch_configuration)

    def add_switch(self, switch: SwitchEntity) -> None:
        """ Adds a configured switch """
        self.switches.append(switch)

    def get_switches(self) -> list[SwitchEntity]:
        """ Creates or gets switches """

        if self.switches_initialised:
            return self.switches

        for switch_configuration in self.switch_configurations:
            self.add_switch(Switch(switch_configuration))

        self.switches_initialised = True

        return self.switches

    def add_sensor_configutaion(self, sensor_configuration):
        """ Adds a sensor configuration to the queue """
        self.sensor_configurations.append(sensor_configuration)

    def add_sensor(self, sensor: SensorEntity) -> None:
        """ Adds a configured sensor """
        self.sensors.append(sensor)

    def get_sensors(self) -> list[SensorEntity]:
        """ Creates or gets sensors """

        if self.sensors_initialised:
            return self.sensors

        # for sensor_configuration in self.sensor_configurations:
            # self.add_sensor(sensor(sensor_configuration))

        self.sensors_initialised = True

        return self.sensors

