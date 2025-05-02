from time import sleep
import requests


def launch(device, *args) -> None:

    print(f"{device.name}: launching fireworks from {device.address}:{device.port}")
    # response = requests.get(f"http://{device.address}:{device.port}/12")


def delayed_launch(device, time: int = 0, *args) -> None:

    sleep(time)

    print(
        f"{device.name}: launching fireworks from {device.address}:{device.port} after {time} seconds"
    )
