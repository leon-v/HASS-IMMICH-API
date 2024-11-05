# Language
from typing import List
from datetime import timedelta
import logging


# HASS
from homeassistant.core import callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

# Local
from .Hub import Hub

# Constants
_LOGGER = logging.getLogger(__name__)

# Need RestEndpoint + RestEndpointSensor

class RestEndpoint(CoordinatorEntity, SensorEntity):
    def __init__(self, hub: Hub, endpoint: str, name: str) -> None:

        from .RestValue import RestValue

        """Init sensor."""
        self.hub: Hub = hub
        self.endpoint: str = endpoint
        self.name: str = name
        self.sensors: List[RestValue] = []

        self._attr_name: str = f"{hub._name} {self.name}"
        self._attr_extra_state_attributes = {}

        self.coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
            self.hub._hass,
            _LOGGER,
            name = f"{name} Coordinator",
            update_method=self.coordinatorUpdate,
            update_interval=timedelta(seconds=5),
        )
        self.listenerRemove = None

        super().__init__(self.coordinator)

    async def async_added_to_hass(self) -> None:
        _LOGGER.debug(f"async_added_to_hass: added callback coordinatorUpdated")
        await super().async_added_to_hass()
        self.listenerRemove = self.coordinator.async_add_listener(self.coordinatorUpdated)

        _LOGGER.debug(f"async_added_to_hass: added callback removedFromHass")
        self.async_on_remove(self.removedFromHass)

    @callback
    def removedFromHass(self):
        if self.listenerRemove:
            self.listenerRemove()

    @callback
    async def coordinatorUpdate(self):
        _LOGGER.debug(f"coordinatorUpdate")
        return await self.hub.api.call('GET', f"/api/{self.endpoint}")

    @callback
    def coordinatorUpdated(self) -> None :
        _LOGGER.debug(f"coordinatorUpdated: {self.coordinator.data}")
        apiResponse = self.coordinator.data
        for sensor in self.sensors:
            sensor.endpointUpdated(apiResponse)


    def registerSensor(self, entity) -> None :
        _LOGGER.debug(f"registerSensor")
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
