import requests


def change_color(device, mode: str = "set", color: str = "on") -> int:

    if mode:
        if mode not in ["set", "fade"]:
            return 2  # bad argument
    if color:
        if color not in ["on", "red", "blue", "green", "yellow", "pink", "cyan", "off"]:
            return 2

    try:
        request = requests.get(
            f"http://{device.address}:{device.port}/{mode}/{color}", timeout=1.5
        )
    except:
        return 1  # request timed out
    if request.status_code != 200:
        return 1  # bad status code

    return 0  # execution successful
