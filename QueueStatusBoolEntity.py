from typing import List

from homeassistant.components.binary_sensor import BinarySensorEntity

from .RestEndpoint import RestEndpoint
from .RestValue import RestValueSensor

class QueueStatusBoolEntity(BinarySensorEntity, RestValueSensor):
    def __init__(
        self,
        endpoint: RestEndpoint,
        path: List[str],
        groupName: str,
        sensorName: str,
        onIcon: str = "mdi:check",
        offIcon: str = "mdi:close"
    ) -> None:
        """Initialize the queue state boolean entity."""
        super().__init__(
            endpoint = endpoint,
            path = path,
            groupName = groupName,
            sensorName = sensorName
        )
        self.onIcon = onIcon
        self.offIcon = offIcon

        self._attr_is_on: bool = False
        self._attr_icon: str = "mdi:loading"

    async def endpointUpdated(self, apiResponse):
        self._attr_is_on = self.getEndpointValue(apiResponse)
        self._attr_icon = self.onIcon if self._attr_is_on else self.offIcon
        self.async_write_ha_state()

