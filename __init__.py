from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .hub import Hub

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS = [Platform.SENSOR, Platform.SWITCH]

type HubConfigEntry = ConfigEntry[Hub]

async def async_setup_entry(hass: HomeAssistant, hub_config_entry: HubConfigEntry) -> bool:
    """Set up from a config entry."""

    hub_config_entry.runtime_data = Hub(
        hass,
        hub_config_entry.data["host"],
        hub_config_entry.data["api_key"]
    )

    await hass.config_entries.async_forward_entry_setups(hub_config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, hub_config_entry: ConfigEntry) -> bool:
    """Unload config entry."""
    return await hass.config_entries.async_unload_platforms(hub_config_entry, PLATFORMS)