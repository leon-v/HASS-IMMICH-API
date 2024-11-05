"""Platform for IMMICH Rest API switch integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
# from homeassistant.components.sensor import SensorEntity
# from homeassistant.components.number import NumberEntity
# from homeassistant.components.binary_sensor import BinarySensorEntity
# from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

from . import HubConfigEntry
from .Constants import DOMAIN
from .Hub import Hub
from .RestEndpoint import RestEndpoint
from .RestRequest import RestRequest
from .RestCommand import RestCommand
from .QueuePauseResumeSwitch import QueuePauseResumeSwitch, RestCommand
from .QueueSizeNumberEntity import QueueSizeNumberEntity
from .QueueStatusBoolEntity import QueueStatusBoolEntity

# from datetime import timedelta
# from typing import List

import logging

_LOGGER = logging.getLogger(__name__)

from .RestValue import RestValue

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add  sensors for passed config_entry in HA."""
    hub: Hub = config_entry.runtime_data

    await hub.jobsSensorEndpoint.coordinator.async_config_entry_first_refresh()

    newDevices = []

    request = RestRequest(
        hub = hub,
        method = "PUT",
        uriPath = "/api/jobs/thumbnailGeneration"
    )

    newDevices.append(QueuePauseResumeSwitch(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'queueStatus', 'isPaused'],
        '- Thumbnail Generation Status',
        '- Paused Switch New',
        onCommand = RestCommand(request, {"command": "pause", "force": False}),
        offCommand = RestCommand(request, {"command": "resume", "force": False}),
        responsePath = ['queueStatus', 'isPaused'],
    ))

    async_add_entities(newDevices)