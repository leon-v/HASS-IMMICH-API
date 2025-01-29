"""Config flow for Hello World integration."""

from __future__ import annotations
import logging
from typing import Any
import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from aiohttp import client_exceptions

from .const import DOMAIN
from .hub import Hub

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
  vol.Required("host"): str,
  vol.Required("api_key"): str,
})


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    host = data["host"]

    if len(host) < 3:
        raise InvalidHost


    hub = Hub(hass, host, data['api_key'])

    try:
        result = await hub.validate_access_token()
    except client_exceptions.ClientResponseError as client_error:
        raise CannotConnect(f"HTTP error occurred: {client_error.status} {client_error.message}") from client_error
    except client_exceptions.InvalidUrlClientError as client_error:
        raise CannotConnect(f"Invalid URL: {host}") from client_error
    if not result:
        raise CannotConnect

    # InvalidAuth

    # Return info that you want to store in the config entry.
    # "Title" is what is displayed to the user for this hub device
    # It is stored internally in HA as part of the device config.
    # See `async_step_user` below for how this is used
    return {
        "title": data["host"],
        "host":  data["host"],
        "api_key":  data["api_key"],
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1
    # Pick one of the available connection classes in homeassistant/config_entries.py
    # This tells HA if it should be asking for updates, or it'll be notified of updates
    # automatically. This example uses PUSH, as the dummy hub will notify HA of
    # changes.
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect as excepttion:
                message = str(excepttion)
                errors["base"] = message if message else "Unknown connection error"
            except InvalidHost as excepttion:
                message = str(excepttion)
                errors["host"] = message if message else "Unknown host error"
            except Exception as excepttion:  # pylint: disable=broad-except
                message = str(excepttion)
                message = message if message else "Unknown error"
                _LOGGER.exception("Unexpected exception: %s", message)
                errors["base"] = message

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    def is_matching(self, other_flow: config_entries.ConfigFlow) -> bool:
        """Return True if other_flow is matching this flow."""
        raise NotImplementedError

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""