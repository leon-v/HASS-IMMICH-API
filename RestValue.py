import logging
from typing import List

from homeassistant.components.sensor import SensorEntity

from .RestEndpoint import RestEndpoint

# Constants
_LOGGER = logging.getLogger(__name__)

class RestValue():
    def __init__(
        self,
        endpoint: RestEndpoint,
        path: List[str]
    ) -> None:
        self.endpoint: RestEndpoint = endpoint
        self.path: List[str] = path
        self.endpoint.registerSensor(self)

    def endpointUpdated(self, apiResponse):
        _LOGGER.error(f"endpointUpdated must be implimented to get updates")
        """Must be extended and call getEndpointValue."""

    def getEndpointValue(self, apiResponse):
        workingValue = apiResponse

        for key in self.path:
            if key not in workingValue:
                self._attr_available = False
                return None

            workingValue = workingValue[key]

        self._attr_available = True
        return workingValue

class RestValueSensor(RestValue, SensorEntity):
    def __init__(
            self,
            endpoint: RestEndpoint,
            path: List[str],
            groupName: str,
            sensorName: str
    ) -> None:
        """Initialize the queue state boolean entity."""
        self.groupName: str = groupName
        self.sensorName: str = sensorName
        self._attr_name: str = f"{endpoint._attr_name} {groupName} {sensorName}"
        super().__init__(endpoint, path)