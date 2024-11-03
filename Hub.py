"""A  'hub' that connects several devices."""

# Language
from __future__ import annotations

# HASS
from homeassistant.core import HomeAssistant

# This Module
from .ImmichApi import ImmichApi

# Constants


class Hub:
    """Dummy hub for Hello World example."""

    manufacturer = "Demonstration Corp"
    instanceIndex = 0

    def __init__(self, hass: HomeAssistant, host: str, api_key: str) -> None:
        """Init dummy hub."""
        self.api: ImmichApi = ImmichApi(host, api_key)
        self._hass = hass

        if (Hub.instanceIndex):
            self._name = f"IMMICH {Hub.instanceIndex}"
        else:
            self._name = "IMMICH"

        Hub.instanceIndex += 1

        self._id = self._name.lower()
        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id