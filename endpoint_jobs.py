"""Jobs API endpoint"""

import logging
import re

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


from .api import ApiClient, Route, ValuePath, Listener
from .endpoint import Endpoint, PollingRequest
from .switch import Switch, SwitchCommand
from .sensor import QueueStatus

_LOGGER = logging.getLogger(__name__)

class Jobs(Endpoint):
    """Jobs IMMICH API endpoint"""
    def __init__(
            self,
            hass: HomeAssistant,
            api_client: ApiClient,
            name_prefix: str,
    ) -> None:
        self.name_prefix: str = name_prefix
        self.coordinator: DataUpdateCoordinator

        super().__init__(hass, api_client)

    async def setup(self):

        jobs = await self.api_client.send(Route('GET', '/api/jobs'))

        polling_request: PollingRequest = self.add_sensor(PollingRequest(
            self.hass,
            self.api_client,
            f"{self.name_prefix} Jobs REST Endpoint",
            Route('GET', '/api/jobs'),
            timedelta(seconds = 5)
        ))

        self.coordinator: DataUpdateCoordinator = polling_request.coordinator

        # Loop through jobs, get key and valiue
        for key, value in jobs.items():

            name = re.sub(r'([a-z])([A-Z])', r'\1 \2', key).title()

            self.add_sensor(QueueStatus(
                f"{name} Queue",
                Listener(
                    coordinator = self.coordinator,
                    value_path = ValuePath([key, 'jobCounts']),
                    attribute_path = ValuePath([key, 'jobCounts']),
                )
            ))

            self.add_switch(
                Switch(
                    f"{name} Queue Enable",
                    SwitchCommand(
                        self.api_client,
                        Route("PUT", f"/api/jobs/{key}", ValuePath(['queueStatus', 'isPaused'])),
                        {"command": "pause", "force": False},
                        {"command": "resume", "force": False}
                    ),
                    Listener(
                        coordinator = self.coordinator,
                        value_path = ValuePath([key, 'queueStatus', 'isPaused']),
                        attribute_path = ValuePath([key, 'queueStatus'])
                    ),
                    invert = True
                )
            )