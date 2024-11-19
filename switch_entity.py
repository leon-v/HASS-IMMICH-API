
from dataclasses import dataclass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import ValuePath, Route, Listener

@dataclass
class SwitchCommand():
    """ All parameters required to interact with a switch """
    def __init__(
        self,
        route: Route,
        on_data: ValuePath,
        off_data: ValuePath
    ) -> None:
        self.route: Route = route
        self.on_data: ValuePath = on_data
        self.off_data: ValuePath = off_data

@dataclass
class SwitchConfiguration():
    """ Hold configutation to initalise a switch """
    def __init__(
        self,
        name: str,
        command: SwitchCommand,
        listener: Listener
    ) -> None:
        self.name: str = name
        self.command: SwitchCommand = command
        self.listener: Listener = listener


class Switch(CoordinatorEntity):
    """ Switch entity class """
    def __init__(self, configuration: SwitchConfiguration):
        pass
