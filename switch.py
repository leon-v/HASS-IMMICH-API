from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HubConfigEntry
from .Hub import Hub
from .RestRequest import RestRequest
from .QueuePauseResumeSwitch import QueuePauseResumeSwitch
from .RestCommand import RestCommand

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add  sensors for passed config_entry in HA."""
    hub: Hub = config_entry.runtime_data

    await hub.jobsSensorEndpoint.coordinator.async_config_entry_first_refresh()

    thumbnailGenerationCommandRequest = RestRequest( hub = hub, method = "PUT", uriPath = "/api/jobs/thumbnailGeneration")
    hub.switches.append(QueuePauseResumeSwitch(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'queueStatus', 'isPaused'],
        '- Thumbnails',
        '- Paused',
        onCommand = RestCommand(thumbnailGenerationCommandRequest, {"command": "pause", "force": False}),
        offCommand = RestCommand(thumbnailGenerationCommandRequest, {"command": "resume", "force": False}),
        responsePath = ['queueStatus', 'isPaused'],
    ))

    async_add_entities(hub.switches)
