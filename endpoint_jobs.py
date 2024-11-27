"""Jobs API endpoint"""

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


from .api import ApiClient, Route, ValuePath, Listener
from .endpoint import Endpoint, PollingRequest
from .switch import Switch, SwitchCommand
from .sensor import QueueStatus

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

        polling_request: PollingRequest = self.add_sensor(PollingRequest(
            self.hass,
            self.api_client,
            f"{self.name_prefix} Jobs REST Endpoint",
            Route('GET', '/api/jobs'),
            timedelta(seconds = 5)
        ))

        self.coordinator: DataUpdateCoordinator = polling_request.coordinator

        self.add_sensor(QueueStatus(
            'Jobs Thumbnials Queue',
            Listener(
                coordinator = self.coordinator,
                value_path = ValuePath(['thumbnailGeneration', 'jobCounts']),
                attribute_path = ValuePath(['thumbnailGeneration', 'jobCounts']),
            )
        ))

        self.add_switch(
            Switch(
                f"{self.name_prefix} Jobs Thumbnials Queue Enabled",
                SwitchCommand(
                    self.api_client,
                    Route("PUT", "/api/jobs/thumbnailGeneration", ValuePath(['queueStatus', 'isPaused'])),
                    {"command": "pause", "force": False},
                    {"command": "resume", "force": False}
                ),
                Listener(
                    coordinator = self.coordinator,
                    value_path = ValuePath(['thumbnailGeneration', 'queueStatus', 'isPaused']),
                    attribute_path = ValuePath(['thumbnailGeneration', 'queueStatus'])
                ),
                invert = True
            )
        )

