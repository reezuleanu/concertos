import requests


def toggle_light(device, toggle: str = "toggle") -> int:
    """Toggle light

    Args:
        device (Device): device data
        toggle (str, optional): toggle mode
        toggle(default) - toggle the light
        on - always turn on
        off - always turn off

    Returns:
        int: execution exit code
    """
    if toggle:
        if toggle not in ["on", "off", "toggle"]:
            return 2  # bad argument
    try:
        request = requests.get(
            f"http://{device.address}:{device.port}/12/{toggle}", timeout=1.5
        )
    except:
        return 1  # request timed out
    if request.status_code != 200:
        return 1  # bad status code

    return 0  # execution successful
