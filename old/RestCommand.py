from typing import Callable, Any

from .RestRequest import RestRequest

import logging
_LOGGER = logging.getLogger(__name__)
#_LOGGER.debug(f"____")

class RestCommand:
    def __init__(self, request: RestRequest, data: object):
        self.request: RestRequest = request
        self.data: object = data
        self.callback: Callable[[Any], None]

    async def run(self):
        _LOGGER.debug(f"Run Command: {self.request.method} {self.request.uriPath} Data: {self.data}")
        apiResponse = await self.request.hub.api.call(
            self.request.method,
            self.request.uriPath,
            json = self.data
        )

        if self.callback:
            _LOGGER.debug(f"Run Callback: {apiResponse}")
            await self.callback(apiResponse)