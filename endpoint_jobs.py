"""Jobs API endpoint"""

from datetime import timedelta

from homeassistant.core import HomeAssistant

from .api import ApiClient, Route, ValuePath, Listener
from .endpoint import Endpoint, PollingRequest
from .switch_entity import Switch, SwitchCommand

class Jobs(Endpoint):
    """Jobs IMMICH API endpoint"""
    def __init__(
            self,
            hass: HomeAssistant,
            api_client: ApiClient,
            name_prefix: str,
    ) -> None:
        self.name_prefix: str = name_prefix

        super().__init__(hass, api_client)

        self.polling_request: PollingRequest = PollingRequest(
            self.hass,
            self.api_client,
            f"{self.name_prefix} Jobs REST Endpoint",
            Route('GET', '/api/jobs'),
            timedelta(seconds = 5)
        )

        self.add_sensor(self.polling_request)

        switch = Switch(
            f"{self.name_prefix} Jobs Thumbnials Queue Enabled",
            SwitchCommand(
                self.api_client,
                Route("PUT", "/api/jobs/thumbnailGeneration", ValuePath(['queueStatus', 'isPaused'])),
                {"command": "pause", "force": False},
                {"command": "resume", "force": False}
            ),
            Listener(
                self.polling_request.coordinator,
                ValuePath(['thumbnailGeneration', 'queueStatus', 'isPaused'])
            ),
            invert = True
        )

        self.add_switch(switch)

