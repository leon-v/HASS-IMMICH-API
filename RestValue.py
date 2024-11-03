from typing import List

from homeassistant.components.sensor import SensorEntity

from .RestEndpoint import RestEndpoint

class RestValue(SensorEntity):

    def __init__(
            self,
            endpoint: RestEndpoint,
            groupName: str,
            sensorName: str,
            path: List[str]
    ) -> None:
        """Initialize the queue state boolean entity."""
        self.endpoint: RestEndpoint = endpoint
        self.groupName: str = groupName
        self.sensorName: str = sensorName
        self.path: List[str] = path
        self.endpoint.registerSensor(self)

    def endpointUpdated(self, apiResponse):
        workingValue = apiResponse

        for key in self.path:
            if key not in workingValue:
                self._attr_available = False
                return

            workingValue = workingValue[key]

        self._attr_available = True
        return workingValue

