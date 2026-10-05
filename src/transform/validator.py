SUPPORTED_TYPES = {
    "int": int,
    "string": str,
    "str": str,
    "float": float,
    "list": list,
    "dict": dict
}

def convert_value(value, type_str:str):
    if value is None:
        return None


    python_type = SUPPORTED_TYPES.get(type_str.lower())

    if python_type is None:
        raise ValueError(f'Type "{type_str}" is not supported')

    try:
        return python_type(value)
    except (ValueError, TypeError):
        return None
