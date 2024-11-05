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

    # TODO jobsSensorEndpoint.addSensor(...), and async_add_entities(jobsSensorEndpoint.getEntities())

    newDevices.append(hub.jobsSensorEndpoint)

    newDevices.append(QueueSizeNumberEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'jobCounts' ,'active'],
        '- Thumbnail Generation Queue',
        '- Active'
    ))

    newDevices.append(QueueSizeNumberEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'jobCounts' ,'failed'],
        '- Thumbnail Generation Queue',
        '- Failed'
    ))

    newDevices.append(QueueSizeNumberEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'jobCounts' ,'waiting'],
        '- Thumbnail Generation Queue',
        '- Waiting'
    ))

    newDevices.append(QueueSizeNumberEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'jobCounts' ,'paused'],
        '- Thumbnail Generation Queue',
        '- Paused'
    ))

    newDevices.append(QueueStatusBoolEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'queueStatus', 'isActive'],
        '- Thumbnail Generation Status',
        '- Active'
    ))

    async_add_entities(newDevices)