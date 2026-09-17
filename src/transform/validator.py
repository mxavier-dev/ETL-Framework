import json

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

    if not python_type:
        raise ValueError(f'Type "{type_str}" is not supported')

    return isinstance(value, python_type)
