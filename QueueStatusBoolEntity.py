from typing import List

from homeassistant.components.binary_sensor import BinarySensorEntity

from .RestEndpoint import RestEndpoint
from .RestValue import RestValue

class QueueStatusBoolEntity(BinarySensorEntity, RestValue):
    def __init__(
            self,
            endpoint: RestEndpoint,
            groupName: str,
            sensorName: str,
            path: List[str],
            onIcon: str = "mdi:check",
            offIcon: str = "mdi:close"
    ) -> None:
        """Initialize the queue state boolean entity."""
        super().__init__(endpoint, groupName, sensorName, path)
        self.onIcon = onIcon
        self.offIcon = offIcon

        self._attr_is_on: bool = False
        self._attr_icon: str = "mdi:loading"

    @property
    def is_on(self) -> bool:
        """Return true if the entity is on (resumed)."""
        return self._attr_is_on

    def endpointUpdated(self, apiResponse):
        self._attr_is_on = self.getEndpointValue(apiResponse)
        self._attr_icon = self.onIcon if self._attr_is_on else self.offIcon
        self.async_write_ha_state()

