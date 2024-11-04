from typing import List

from homeassistant.components.number import NumberEntity

from .RestEndpoint import RestEndpoint
from .RestValue import RestValue

class QueueSizeNumberEntity(NumberEntity, RestValue):
    def __init__(self, endpoint: RestEndpoint, groupName: str, sensorName: str, path: List[str]) -> None:
        """Initialize the queue size number entity."""
        super().__init__(endpoint, groupName, sensorName, path)
        self._attr_icon: str = "mdi:counter"

    def endpointUpdated(self, apiResponse):
        self._attr_native_value = self.getEndpointValue(apiResponse)
        self.async_write_ha_state()