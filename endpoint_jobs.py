"""Jobs API endpoint"""

from datetime import timedelta

from homeassistant.core import HomeAssistant

from .api import ApiClient, Route, ValuePath, Listener
from .endpoint import Endpoint, Request, PollingRequest
from .switch_entity import SwitchConfiguration, SwitchCommand

class Jobs(Endpoint):
    """Jobs IMMICH API endpoint"""
    def __init__(
            self,
            hass: HomeAssistant,
            api_client: ApiClient
    ) -> None:

        super().__init__(hass, api_client)

        self.polling_request: PollingRequest = PollingRequest(
            self.hass,
            self.api_client,
            Route('GET', '/jobs'),
            timedelta(seconds=5)
        )

        self.switch_configurations.append(
            SwitchConfiguration(
                'Thumbnials',
                SwitchCommand(
                    self.api_client,
                    Route("PUT", "/api/jobs/thumbnailGeneration", ValuePath(['queueStatus', 'isPaused'])),
                    {"command": "pause", "force": False},
                    {"command": "resume", "force": False}
                ),
                Listener(
                    self.polling_request.coordinator,
                    ValuePath(['thumbnailGeneration', 'queueStatus', 'isPaused'])
                )
            )
        )