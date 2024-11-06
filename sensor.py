"""Platform for IMMICH Rest API sensor integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HubConfigEntry
from .Hub import Hub
from .QueueSizeNumberEntity import QueueSizeNumberEntity
from .QueueStatusBoolEntity import QueueStatusBoolEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add  sensors for passed config_entry in HA."""
    hub: Hub = config_entry.runtime_data

    await hub.jobsSensorEndpoint.coordinator.async_config_entry_first_refresh()

    hub.sensors.append(QueueSizeNumberEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'jobCounts' ,'active'],
        '- Thumbnails',
        '- Active'
    ))

    hub.sensors.append(QueueSizeNumberEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'jobCounts' ,'failed'],
        '- Thumbnail',
        '- Failed'
    ))

    hub.sensors.append(QueueSizeNumberEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'jobCounts' ,'waiting'],
        '- Thumbnail',
        '- Waiting'
    ))

    hub.sensors.append(QueueSizeNumberEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'jobCounts' ,'paused'],
        '- Thumbnail',
        '- Paused'
    ))

    hub.sensors.append(QueueStatusBoolEntity(
        hub.jobsSensorEndpoint,
        ['thumbnailGeneration', 'queueStatus', 'isActive'],
        '- Thumbnails',
        '- Active'
    ))

    async_add_entities(hub.sensors)