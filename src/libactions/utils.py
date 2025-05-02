def get_dict_key(dict: dict, value: any) -> any:
    """Return the key from a dict for a specific value

    Args:
        dict (dict): dict to search through
        value (any): value to find key for

    Returns:
        any: key for that value
    """

    for k, v in dict.items():
        if v == value:
            return k
    return None  # base case
