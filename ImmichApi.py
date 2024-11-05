import logging

from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)

class ImmichApi:

    def __init__(self, host, apiKey):
        self.host: str = host
        self.headers = {"x-api-key": apiKey}

    async def call(self, method: str, endpoint: str, **kwargs):
        async with ClientSession() as session:
            _LOGGER.debug(f"Request: Method: {method} URL: {self.host}{endpoint} kwargs: {kwargs}")
            async with session.request(
                method=method,
                url=f"{self.host}{endpoint}",
                headers=self.headers,
                **kwargs
            ) as response:
                _LOGGER.debug(f"Response: Status: {response.status}")
                response.raise_for_status()
                return await response.json()

    # /api/auth/validateToken
    # https://immich.app/docs/api/validate-access-token
    # {"authStatus":true}
    async def validateAccessToken(self):
        response = await self.call("POST", "/api/auth/validateToken")
        return response["authStatus"] == True
