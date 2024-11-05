from typing import List
import logging

from homeassistant.components.switch import SwitchEntity

from .RestEndpoint import RestEndpoint
from .RestCommand import RestCommand

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
        self._attr_name: str = f"{endpoint._attr_name} {groupName} {sensorName}"

        self.onCommand: RestCommand = onCommand
        self.onCommand.callback = self.commandUpdated

        self.offCommand: RestCommand = offCommand
        self.offCommand.callback = self.commandUpdated
        self.responsePath: List[str] = responsePath

        self._attr_should_poll = False
        self._attr_is_on = False
        self._attr_available = True

        self.endpoint.registerSensor(self)

    async def async_turn_on(self, **kwargs):
        self._attr_is_on = True
        await self.onCommand.run()
        self.schedule_update_ha_state()


    async def async_turn_off(self, **kwargs):
        self._attr_is_on = False
        await self.offCommand.run()
        self.schedule_update_ha_state()


    async def commandUpdated(self, apiResponse):
        _LOGGER.debug(f"commandUpdated: {apiResponse}")
        self.updateFromApiResponse(self, self.responsePath, apiResponse)
        self.schedule_update_ha_state()


    async def endpointUpdated(self, apiResponse):
        _LOGGER.debug(f"endpointUpdated: {apiResponse}")
        self.updateFromApiResponse(self, self.path, apiResponse)
        self.schedule_update_ha_state()


    def updateFromApiResponse(self, path: List[str], apiValue):
        isOn = self.getApiResponseValue(path, apiValue)
        self.setIsOn(isOn)


    def setIsOn(self, isOn):
        self._attr_available = False if isOn == None else True
        self._attr_is_on = isOn
        _LOGGER.debug(f"setIsOn: {isOn}")


    def getApiResponseValue(self, path: List[str], apiValue):
        for key in self.responsePath:
            if key not in apiValue:
                return None
            apiValue = apiValue[key]
        return apiValue