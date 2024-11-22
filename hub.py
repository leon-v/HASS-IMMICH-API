"""A  'hub' that connects several devices."""

from __future__ import annotations
import logging
from homeassistant.core import HomeAssistant


_LOGGER = logging.getLogger(__name__)

class Hub:
    """Device continer for all sensors."""

    manufacturer = "IMMICH by the IMMICH core team. This component by Leon-V"

    def __init__(self, hass: HomeAssistant, host: str, api_key: str) -> None:
        """Init hub for IMMICH API"""

        self.hass: HomeAssistant = hass

        from .api import ApiClient
        self.api: ApiClient = ApiClient(host, api_key)

        from .endpoint import Endpoint
        self.endpoints: list[Endpoint] = []

        self._name: str = "IMMICH 1"
        self._id: str = self._name.lower()

        from .endpoint_jobs import Jobs
        self.endpoints.append(Jobs(self))

        self.online = True

    @property
    def hub_id(self: Hub) -> str:
        """ID for dummy hub."""
        return self._id

    async def validate_access_token(self) -> bool:
        """Validates that the API is making requests and authenticating"""
        from .api import Route
        return await self.api.send(Route('POST', '/api/auth/validateToken', ['authStatus']))
