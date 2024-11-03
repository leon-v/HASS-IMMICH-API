import logging

from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)

class ImmichApi:

    def __init__(self, host, apiKey):
        self.host: str = host
        self.headers = {"x-api-key": apiKey}

    async def call(self, method, endpoint, **kwargs):
        async with ClientSession() as session:
            _LOGGER.debug(f"Request:\nMethod: {method} URL: {self.host}{endpoint}\nHeaders: {self.headers}\nkwargs: {kwargs}")
            async with session.request(
                method=method,
                url=f"{self.host}{endpoint}",
                headers=self.headers,
                **kwargs
            ) as response:
                responseText = await response.text()
                _LOGGER.debug(f"Response: Status: {response.status}\nHeaders: {response.headers}\nBody: {responseText}")
                response.raise_for_status()
                return await response.json()

    # /api/auth/validateToken
    # https://immich.app/docs/api/validate-access-token
    # {"authStatus":true}
    async def validateAccessToken(self):
        response = await self.call("POST", "/api/auth/validateToken")
        return response["authStatus"] == True

    # https://immich.app/docs/api/send-job-command
    async def sendJobCommand(self, id, command, force):
        response = await self.call(
            method="PUT",
            endpoint=f"/api/jobs/{id}",
            json={
                "command": command,
                "force": force
            }
        )
        return response["queueStatus"]["isPaused"]

    async def getSmartSearchIsPaused(self):
        response = await self.call("GET", "/api/jobs")
        return response["smartSearch"]["queueStatus"]["isPaused"]

    async def getJobs(self):
        return await self.call("GET", "/api/jobs")
