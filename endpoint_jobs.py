"""Jobs API endpoint"""

from .hub import Hub
from .api import Route, ValuePath
from .endpoint import Endpoint, Request, PollingRequest, Listener
from .switch import SwitchConfiguration, SwitchCommand

class Jobs(Endpoint):
    """Jobs IMMICH API endpoint"""
    def __init__(self, hub: Hub):

        super().__init__(hub)

        self.polling_request: Request = PollingRequest(self.hub, Route('GET', '/jobs'), 5)

        self.switch_configurations.append(
            SwitchConfiguration(
                'Thumbnials',
                SwitchCommand(
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