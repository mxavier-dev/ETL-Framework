def validate_type(value, type_str:str) -> bool:
    type_map = {
        "int": int,
        "string": str,
        "str": str,
        "float": float,
        "bool": bool,
        "boolean": bool,
        "list": list,
        "dict": dict
    }

    python_type = type_map.get(type_str.lower())

    if python_type is None:
        raise ValueError(f'Type "{type_str}" is not supported')

    try:
        python_type(value)
        return True
    except (ValueError, TypeError):
        return False
