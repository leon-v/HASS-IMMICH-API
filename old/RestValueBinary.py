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
        super().__init__()
        self.endpoint: RestEndpoint = endpoint
        self.groupName: str = groupName
        self.sensorName: str = sensorName
        self.path: List[str] = path
        self.onIcon = onIcon
        self.offIcon = offIcon

        self._attr_name: str = f"{endpoint._attr_name} {groupName} {sensorName}"
        self._attr_is_on: bool = False
        self._attr_icon: str = "mdi:loading"

        # self.endpoint.registerSensor(self)

    @property
    def is_on(self) -> bool:
        """Return true if the entity is on (resumed)."""
        return self._attr_is_on
