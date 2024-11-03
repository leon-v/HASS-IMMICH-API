from typing import List

from homeassistant.components.number import NumberEntity

from .RestEndpoint import RestEndpoint

class QueueSizeNumberEntity(NumberEntity):
    def __init__(self, endpoint: RestEndpoint, groupName: str, sensorName: str, path: List[str]) -> None:
        """Initialize the queue size number entity."""
        self.endpoint: RestEndpoint = endpoint
        self.groupName = groupName
        self.sensorName: str = sensorName
        self.path: List[str] = path

        self._attr_name: str = f"{endpoint._attr_name} {groupName} {sensorName}"
        self._attr_icon: str = "mdi:counter"

        self.endpoint.registerSensor(self)

    def endpointUpdated(self, apiResponse):
        workingValue = apiResponse

        for key in self.path:
            if key not in workingValue:
                self._attr_available = False
                self._attr_native_value = None
                self.async_write_ha_state()
                return

            workingValue = workingValue[key]

        self._attr_available = True
        self._attr_native_value = workingValue
        self.async_write_ha_state()