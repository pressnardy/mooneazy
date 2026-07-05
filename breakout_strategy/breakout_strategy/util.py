def resolve_level(level):
    """
    extracts level values for levels passed as dicts
    and return a list of int
    """
    if isinstance(level, dict):
        level = level["value"]
    return level

