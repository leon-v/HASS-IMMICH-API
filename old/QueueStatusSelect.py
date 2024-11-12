from homeassistant.components.select import SelectEntity



class QueueStatusSelect(SelectEntity):
    def __init__(self, endpoint: RestEndpoint, name: str, key: str):
        self._endpoint = endpoint
        self._name = name
        self._key = key
        self._options = ["active", "paused", "stopped"]
        self._current_option = "active"

    @property
    def name(self):
        return self._name

    @property
    def options(self):
        return self._options

    @property
    def current_option(self):
        return self._current_option

    async def async_select_option(self, option: str):
        await self._endpoint.set_queue_state(self._key, option)
        self._current_option = option
        self.async_write_ha_state()

    async def async_update(self):
        state = await self._endpoint.get_queue_state(self._key)
        self._current_option = state['status']