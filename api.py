"""API methods for sending HTTP requests."""

import logging
from datetime import timedelta
from aiohttp import ClientSession
from aiohttp.client import _RequestOptions
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from .hub import Hub

_LOGGER = logging.getLogger(__name__)

class Route:
    """API route configuration (method and URI path)"""
    def __init__(self, method: str, uri: str):
        self.method: str = method
        self.uri: str = uri

class HttpRequest:
    """Makes HTTP requests"""
    def __init__(self, hub: Hub, route: Route):
        self.hub: Hub = hub
        self.route: Route = route

        self.host: str
        self.api_key: str

        self.headers = {"x-api-key": self.api_key}

    async def send(self, request_options: _RequestOptions):
        """Sends the configured HTTP request"""
        url = self.host + self.route.uri
        async with ClientSession() as session:
            _LOGGER.debug(
                "Request: Method: %s URL: %s kwargs: %s",
                self.route.method,
                url,
                request_options
            )
            async with session.request(
                method=self.route.method,
                url=url,
                headers=self.headers,
                **request_options
            ) as response:
                _LOGGER.debug("Response: Status: %s", response.status)
                response.raise_for_status()
                return await response.json()

class PollingRequest(HttpRequest, CoordinatorEntity):
    """ Sends a HTTP request on an interval"""
    def __init__(self, hub: Hub, route: Route, interval: timedelta, request_options: _RequestOptions):

        HttpRequest.__init__(self, hub, route)

        self.request_options: _RequestOptions = request_options
        self.coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
            self.hub._hass,
            _LOGGER,
            name = f"{self.route.uri} Coordinator",
            update_method=self.coordinator_update,
            update_interval=interval,
        )

        CoordinatorEntity.__init__(self, self.coordinator)

    @callback
    async def coordinator_update(self):
        """Performs the HTTP request when coordinator requests an update"""
        return await self.send(self.request_options)

class CommandRequest(HttpRequest):
    """ Sends a single HTTP request """
    def __init__(self, hub: Hub, route: Route, body: object):
        HttpRequest.__init__(self, hub, route)