"""API methods for sending HTTP requests."""

from __future__ import annotations
from typing import Any
import logging
from aiohttp import ClientSession
from aiohttp.client import _RequestOptions
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class ValuePath:
    """ Hold the expression to traverse to a JSON response node """
    def __init__(self, path: list[str]):
        self.path: list[str] = path

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


    async def send(self, route: Route, request_options: _RequestOptions = None) -> Any:
        """Sends the configured HTTP request"""

        url = self.host + route.uri

        if request_options is None:
            request_options = {}

        session: ClientSession = ClientSession()

        _LOGGER.debug(
            "Request: Method: %s URL: %s request_options: %s",
            route.method,
            url,
            request_options
        )

        try:
            response = await session.request(
                method=route.method,
                url=url,
                headers=self.headers,
                **request_options
            )

            _LOGGER.debug("Response: %s", response)
            response.raise_for_status()
            response_data = await response.json()
            return route.parse_response(response_data)

        finally:
            await session.close()

# class Api():
#     """Sends HTTP requests and parses the response."""

#     def __init__(self, host: str, api_key: str) -> None:
#         """Init hub for IMMICH API"""

#         self.host: str = host
#         self.api_key: str = api_key
#         self.headers = {"x-api-key": api_key}

#     async def send(self, route: Route, request_options: _RequestOptions = None):
#         """Sends the configured HTTP request"""
#         url = f"{self.host}{route.uri}"
#         async with ClientSession() as session:

#             _LOGGER.debug(
#                 "Request: Method: %s URL: %s kwargs: %s",
#                 route.method,
#                 url,
#                 request_options
#             )

#             async with session.request(
#                 method = route.method,
#                 url = url,
#                 headers = self.headers,
#                 **request_options
#             ) as response:
#                 _LOGGER.debug("Response: %s", response)
#                 response.raise_for_status()
#                 response_data = await response.json()
#                 return route.parse_response(response_data)

class Listener:
    """ Used to rute responses to callbacks  """
    def __init__(self, coordinator: DataUpdateCoordinator, value_path: ValuePath) -> None:
        self.coordinator: DataUpdateCoordinator = coordinator
        self.value_path: ValuePath = value_path