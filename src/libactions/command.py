from abc import ABC, abstractmethod
from .device import Device


class Command(ABC):
    def __init__(self, name: str, function: callable, args: list[any]) -> None:
        self.name = name
        self.function = function
        self.args = args

    @abstractmethod
    def exec(self) -> None:
        raise NotImplementedError


class HardwareCommand(Command):
    """Class containing a function, it's arguments, and the device to execute it on"""

    def __init__(
        self, name: str, function: callable, args: list[any], device: Device
    ) -> None:
        super().__init__(name, function, args)
        self.device = device

    def exec(self) -> None:
        """Execute command with required arguments on device"""
        self.function(self.device, *self.args)


class SoftwareCommand(Command):
    """Class containing a function to execute on the database"""

    def __init__(
        self,
        name: str,
        function: callable,
        args: list[any],
        # eventid: int,
    ) -> None:
        super().__init__(name, function, args)
        # self.eventid = eventid

    def exec(self) -> None:
        """Execute command upon the database"""
        self.function(*self.args)
