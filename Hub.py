"""A  'hub' that connects several devices."""

# Language
from __future__ import annotations
from typing import List

# HASS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity, ToggleEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.sensor import SensorEntity


from .ImmichApi import ImmichApi


import logging
_LOGGER = logging.getLogger(__name__)

class Hub:
    """Device continer for all sensors."""

    manufacturer = "IMMICH by the IMMICH core team. This component by Leon-V"

    def __init__(self, hass: HomeAssistant, host: str, api_key: str) -> None:
        """Init dummy hub."""
        self.api: ImmichApi = ImmichApi(host, api_key)
        self._hass = hass
        self._name = "IMMICH"

        self._id = self._name.lower()
        self.online = True

        from .RestEndpoint import RestEndpoint
        self.endpoints: List[RestEndpoint] = []
        self.endpointsCreated = False

        self.entities:  List[Entity] = []
        self.entitiesCreated = False


    async def endpointsFirstRefresh(self):

        self.createEntities()

        for endpoint in self.endpoints:
            await endpoint.coordinator.async_config_entry_first_refresh()


    def createEntities(self) -> None:

        if self.entitiesCreated:
            return

        self.createEndpoints()

        for endpoint in self.endpoints:
            self.entities.append(endpoint)
            self.entities.extend(endpoint.getEntities())

        self.entitiesCreated = True


    def createEndpoints(self) -> None:

        if self.endpointsCreated:
            return

        from .Jobs import Jobs
        self.endpoints.append(Jobs(self))

        self.endpointsCreated = True


    def getSwitches(self) -> List[ToggleEntity]:

        self.createEntities()

        switchEntities: List[ToggleEntity] = []

        for entity in self.entities:
            if isinstance(entity, ToggleEntity):
                switchEntities.append(entity)

        _LOGGER.debug(f"getSwitches {switchEntities}")
        return switchEntities


    def getSensors(self) -> List[SensorEntity,NumberEntity]:

        self.createEntities()

        sensorEntities: List[SensorEntity,NumberEntity] = []

        for entity in self.entities:
            if isinstance(entity, SensorEntity):
                sensorEntities.append(entity)

        return sensorEntities


    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id