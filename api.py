"""API methods for sending HTTP requests."""

from __future__ import annotations
from typing import Any
import logging
from aiohttp import ClientSession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class ValuePath:
    """ Hold the expression to traverse to a JSON response node """
    def __init__(self, path: list[str]):
        self.path: list[str] = path

    def __iter__(self):
        return iter(self.path)

    def __getitem__(self, index):
        return self.path[index]

    def __len__(self):
        return len(self.path)

class Route:
    """API route configuration (method and URI path)"""
    def __init__(self, method: str, uri: str, value_path: ValuePath = None) -> None:
        self.method: str = method
        self.uri: str = uri
        self.value_path: ValuePath = value_path

    def parse_response(self, response_value: Any) -> Any:
        """Returns the node value targeted by value_path"""

        if not self.value_path:
            return response_value

        for key in self.value_path:
            if key not in response_value:
                return None

            response_value = response_value[key]

        return response_value

class ApiClient:
    """Sends HTTP requests."""
    def __init__(self, host: str, api_key: str) -> None:
        self.host: str = host
        self.api_key: str = api_key
        self.headers = {"x-api-key": api_key}


    async def send(self, route: Route, **request_arguments) -> Any:
        """Sends the configured HTTP request"""

        url = self.host + route.uri

        session: ClientSession = ClientSession()

        _LOGGER.debug(
            "Request: Method: %s URL: %s request_arguments: %s",
            route.method,
            url,
            request_arguments
        )

        try:
            response = await session.request(
                method = route.method,
                url = url,
                headers = self.headers,
                **request_arguments
            )

            _LOGGER.debug("Response: %s", await response.text())
            response.raise_for_status()
            response_data = await response.json()
            return route.parse_response(response_data)

        finally:
            await session.close()

class Listener:
    """ Used to rute responses to callbacks  """
    def __init__(self, coordinator: DataUpdateCoordinator, value_path: ValuePath, attribute_path: ValuePath) -> None:
        self.coordinator: DataUpdateCoordinator = coordinator
        self.value_path: ValuePath = value_path
        self.attribute_path: ValuePath = attribute_path

    def parse_response_attribute(self, response_value: Any) -> Any:
        """Returns the node value targeted by value_path"""

        if not self.attribute_path:
            return None

        for key in self.attribute_path:
            if key not in response_value:
                return None

            response_value = response_value[key]

        return response_value

    def parse_response_value(self, response_value: Any) -> Any:
        """Returns the node value targeted by value_path"""

        if not self.value_path:
            return response_value

        for key in self.value_path:
            if key not in response_value:
                return None

            response_value = response_value[key]

        return response_value
