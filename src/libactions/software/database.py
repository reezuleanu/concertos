import requests
from time import sleep

# give django time at the start of execution to acquire it's ip
sleep(1)


def edit_variable(
    event_id: int,
    user_id: int,
    variable_name: str,
    mode: str,
    variable_value: int,
    *args,
) -> int:

    # print(variable_name, variable_value, mode, user_id)
    try:
        response = requests.put(
            f"http://127.0.0.1:8000/events/{event_id}/actions/variables/global/{variable_name}",
            json={"mode": mode, "value": int(variable_value)},
            timeout=1.5,
        )
    except:
        return 1
    if response.status_code != 200:
        return 1

    return 0
