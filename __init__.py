from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .hub import Hub
type HubConfigEntry = ConfigEntry[Hub]
from .logging import setup_logging

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS = [Platform.SWITCH, Platform.SENSOR]

def setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up component."""
    setup_logging()
    return True


async def async_setup_entry(hass: HomeAssistant, hub_config_entry: HubConfigEntry) -> bool:
    """Set up from a config entry."""

    hub = Hub(
        hass,
        hub_config_entry.data["host"],
        hub_config_entry.data["api_key"]
    )

    await hub.setup()

    hub_config_entry.runtime_data = hub

    await hass.config_entries.async_forward_entry_setups(hub_config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, hub_config_entry: HubConfigEntry) -> bool:
    """Unload config entry."""
    return await hass.config_entries.async_unload_platforms(hub_config_entry, PLATFORMS)