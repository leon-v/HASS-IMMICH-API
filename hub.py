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
        self.hass = hass
        self._name = "IMMICH"

        self._id = self._name.lower()
        self.online = True


    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id