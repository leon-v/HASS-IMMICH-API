"""Platform for IMMICH Rest API sensor integration."""

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

    newDevices = []


    jobsEndpoint = RestEndpoint(hub, 'jobs', 'Jobs')

    await jobsEndpoint.coordinator.async_config_entry_first_refresh()

    # TODO jobsEndpoint.addSensor(...), and async_add_entities(jobsEndpoint.getEntities())

    #{"thumbnailGeneration":{"jobCounts":{"active":0,"completed":0,"failed":0,"delayed":0,"waiting":0,"paused":0},"queueStatus":{"isActive":false,"isPaused":false}}
    newDevices.append(QueueSizeNumberEntity(jobsEndpoint, '- Thumbnail Generation Queue', '- Active', ['thumbnailGeneration', 'jobCounts' ,'active']))
    newDevices.append(QueueSizeNumberEntity(jobsEndpoint, '- Thumbnail Generation Queue', '- Completed', ['thumbnailGeneration', 'jobCounts' ,'completed']))
    newDevices.append(QueueSizeNumberEntity(jobsEndpoint, '- Thumbnail Generation Queue', '- Failed', ['thumbnailGeneration', 'jobCounts' ,'failed']))
    # newDevices.append(QueueSizeNumberEntity(jobsEndpoint, '- Thumbnail Generation Queue', '- Delayed', ['thumbnailGeneration', 'jobCounts' ,'delayed']))
    # newDevices.append(QueueSizeNumberEntity(jobsEndpoint, '- Thumbnail Generation Queue', '- Waiting', ['thumbnailGeneration', 'jobCounts' ,'waiting']))
    newDevices.append(QueueSizeNumberEntity(jobsEndpoint, '- Thumbnail Generation Queue', 'Paused', ['thumbnailGeneration', 'jobCounts' ,'paused']))
    newDevices.append(QueueStatusBoolEntity(jobsEndpoint, '- Thumbnail Generation Status', '- Active', ['thumbnailGeneration', 'queueStatus', 'isActive']))
    newDevices.append(QueueStatusBoolEntity(jobsEndpoint, '- Thumbnail Generation Status', '- Paused', ['thumbnailGeneration', 'queueStatus', 'isPaused']))

    newDevices.append(jobsEndpoint)

    async_add_entities(newDevices)