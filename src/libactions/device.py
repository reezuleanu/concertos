from dataclasses import dataclass


@dataclass
class Device:
    """Class for storing info about object"""

    id: int  # database id
    name: str
    type: str
    address: str
    port: int


# name: "lansator rachete"
# type: "rocket_launcher"
# address: "10.0.0.1"
# port: 6969
