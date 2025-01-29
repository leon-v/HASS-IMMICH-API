"""Platform for IMMICH Rest API sensor integration."""


import logging

from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.text import TextEntity

from . import HubConfigEntry
from .hub import Hub
from .endpoint import Endpoint
from .api import Listener

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    hub_config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors to HA."""
    hub: Hub = hub_config_entry.runtime_data

    _LOGGER.debug(
        "hub.endpoints %s",
        hub.endpoints
    )

    endpoint: Endpoint
    sensors: list[SensorEntity] = []

    for endpoint in hub.endpoints:
        sensors.extend(endpoint.get_sensors())

    async_add_entities(sensors)

class QueueStatus(CoordinatorEntity, TextEntity):
    """ Shows the queue size """
    def __init__(self, name: str, listener: Listener):

        self.listener: Listener = listener

        self._attr_name = name
        self._attr_unique_id = self._attr_name.lower().replace(" ", "_")
        self._attr_native_value = 'TEST'
        self._attr_icon = "mdi:queue"

        TextEntity.__init__(self)

        CoordinatorEntity.__init__(self, self.listener.coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        queue_status = self.listener.parse_response_value(self.coordinator.data)

        _LOGGER.info("[%s] Coordinator Update: %s", self._attr_unique_id, queue_status)

        if (queue_status is None):
            self._attr_available = False
            return

        witing = queue_status['waiting'] + queue_status['paused']

        value = f"{queue_status['active']} / {witing}"

        self._attr_native_value = value

        super()._handle_coordinator_update()

    async def async_set_value(self, value: str) -> None:
        """Set the text value."""
        await self.hass.async_add_executor_job(self.set_value, value)

    def set_value(self, value: str) -> None:
        """Change the value."""
        raise NotImplementedError
