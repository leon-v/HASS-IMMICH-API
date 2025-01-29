from typing import List

from homeassistant.components.switch import SwitchEntity

from .RestEndpoint import RestEndpoint
from .RestCommand import RestCommand

import logging
_LOGGER = logging.getLogger(__name__)

class QueuePauseResumeSwitch(SwitchEntity):
    def __init__(
            self,
            endpoint: RestEndpoint,
            path: List[str],
            groupName: str,
            sensorName: str,
            onCommand: RestCommand,
            offCommand: RestCommand,
            responsePath: List[str],
    ):
        self.endpoint: RestEndpoint = endpoint
        self.path: List[str] = path
        self.groupName: str = groupName
        self.sensorName: str = sensorName

        self.onCommand: RestCommand = onCommand
        self.onCommand.callback = self.commandUpdated

        self.offCommand: RestCommand = offCommand
        self.offCommand.callback = self.commandUpdated
        self.responsePath: List[str] = responsePath

        self._attr_name: str = f"{endpoint._attr_name} {groupName} {sensorName}"
        self._attr_should_poll = False
        self._attr_is_on = False
        self._attr_available = True

        self.endpoint.registerSensor(self)

    async def async_turn_on(self, **kwargs):
        _LOGGER.debug(f"Command On")
        self._attr_is_on = True
        await self.onCommand.run()
        self.schedule_update_ha_state()


    async def async_turn_off(self, **kwargs):
        _LOGGER.debug(f"Command Off")
        self._attr_is_on = False
        await self.offCommand.run()


    async def commandUpdated(self, apiResponse):
        self.updateFromApiResponse(self.responsePath, apiResponse)
        _LOGGER.debug(f"Command Update: isOn: {self._attr_is_on}, isAvailable: {self._attr_available}")


    def endpointUpdated(self, apiResponse):
        self.updateFromApiResponse(self.path, apiResponse)
        _LOGGER.debug(f"Poll Update: isOn: {self._attr_is_on}, isAvailable: {self._attr_available}")


    def updateFromApiResponse(self, path: List[str], apiValue):
        isOn = self.getApiResponseValue(path, apiValue)
        self.setIsOn(isOn)


    def setIsOn(self, isOn):
        self._attr_available = isOn != None
        self._attr_is_on = isOn
        self.schedule_update_ha_state()


    def getApiResponseValue(self, path: List[str], apiValue):
        for key in path:
            if key not in apiValue:
                return None
            apiValue = apiValue[key]
        return apiValue