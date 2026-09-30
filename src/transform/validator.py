def convert_value(value, type_str:str) -> bool:
    if value is None:
        return None

    type_map = {
        "int": int,
        "string": str,
        "str": str,
        "float": float,
        # "bool": bool,
        # "boolean": bool,
        "list": list,
        "dict": dict
    }

    python_type = type_map.get(type_str.lower())

    if python_type is None:
        raise ValueError(f'Type "{type_str}" is not supported')

    try:
        return python_type(value)
    except (ValueError, TypeError):
        return None
