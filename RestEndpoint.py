# Language
from typing import List
from datetime import timedelta
import logging


# HASS
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

# Local
from .Hub import Hub

# Constants
_LOGGER = logging.getLogger(__name__)

class RestEndpoint(CoordinatorEntity, SensorEntity):
    def __init__(self, hub: Hub, endpoint: str, name: str) -> None:

        from .RestValue import RestValue

        """Init sensor."""
        self.hub: Hub = hub
        self.endpoint: str = endpoint
        self.name: str = name
        self.sensors: List[RestValue] = []

        self._attr_name: str = f"{hub._name} {self.name}"

        self.coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
            self.hub._hass,
            _LOGGER,
            name = endpoint,
            update_method=self.coordinatorUpdateCallback,
            update_interval=timedelta(seconds=5),
        )
        super().__init__(self.coordinator)
        self._attr_extra_state_attributes = {}

    async def coordinatorUpdateCallback(self):
        """Fetch data from API endpoint."""
        apiResponse = await self.hub.api.call('GET', f"/api/{self.endpoint}")
        for sensor in self.sensors:
            sensor.endpointUpdated(apiResponse)
            sensor.async_write_ha_state()

        return apiResponse

    def registerSensor(self, entity):
        self.sensors.append(entity)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data

    @property
    def state(self):
        """Return the state of the sensor."""
        return 'ok' if self.coordinator.data else 'unavailable'

    @property
    def available(self):
        """Return True if entity is available."""
        return self.state == 'ok'
