SUPPORTED_TYPES = {
    "int": int,
    "string": str,
    "str": str,
    "float": float,
    "bool": bool,
    "boolean": bool,
    "list": list,
    "dict": dict,
    "tuple": tuple
}

def convert_value(value, type_str:str):
    if value is None:
        return None


    python_type = SUPPORTED_TYPES.get(type_str.lower())

    if python_type is None:
        raise ValueError(f'Type "{type_str}" is not supported')

    if python_type is bool:
        if value in ['true', 'True']:
            return True
        elif value in ['false', 'False']:
            return False
        else:
            return None

    if python_type in [tuple, list, dict]:
        if isinstance(value, python_type):
            return value
        else:
            return None

    try:
        return python_type(value)
    except (ValueError, TypeError):
        return None
