from typing import List

from homeassistant.components.number import NumberEntity

from .RestEndpoint import RestEndpoint
from .RestValue import RestValueSensor

class QueueSizeNumberEntity(NumberEntity, RestValueSensor):
    def __init__(
            self,
            endpoint: RestEndpoint,
            path: List[str],
            groupName: str,
            sensorName: str
        ) -> None:
        """Initialize the queue size number entity."""
        super().__init__(
            endpoint = endpoint,
            path = path,
            groupName = groupName,
            sensorName = sensorName
        )
        self._attr_icon: str = "mdi:counter"

    def endpointUpdated(self, apiResponse):
        self._attr_native_value = self.getEndpointValue(apiResponse)
        self.async_write_ha_state()