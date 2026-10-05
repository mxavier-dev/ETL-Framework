from src.transform.validator import SUPPORTED_TYPES
from src.transform.cleaner import TRANSFORMATIONS

SUPPORTED_FIELDS = [
    'type',
    'clean',
    'transform',
    'min',
    'max',
    'source',
    'contains'
]

def validate_schema(schema):
    for key, values in schema.items():
        for field in values:
            if field not in SUPPORTED_FIELDS:
                raise ValueError(
                    f'Unsupported field "{field}"'
                )

        if not schema[key].get('type'):
            raise ValueError(
                f'Field "{key}": "type" field has to exist'
            )

        if schema[key]['type'] not in SUPPORTED_TYPES:
            raise ValueError(
                f'Unsupported type "{schema[key]["type"]}"'
            )

        clean = values.get('clean')
        transform = values.get('transform')

        if clean is not None and not isinstance(clean, bool):
            raise ValueError(
                f'Field "{key}": "clean" has to be a boolean (true, false)'
            )

        if clean is True and not transform:
            raise ValueError(
                f'Field "{key}": "clean" requires a "transform" field'
            )

        if transform and clean is not True:
            raise ValueError(
                f'Field "{key}": "transform" requires "clean": true'
            )

        if values.get('transform') is not None and values.get('transform') not in TRANSFORMATIONS:
            raise ValueError(
                f'Field "{key}": unsupported transform "{values.get("transform")}"'
            )

        if values['type'] == 'int':
            for field in ['min', 'max']:
                if field in values and not isinstance(values[field], int):
                    raise ValueError(
                        f'Field "{key}": "{field}" has to be an integer'
                    )

        if values['type'] == 'float':
            for field in ['min', 'max']:
                if field in values and not isinstance(values[field], (int, float)):
                    raise ValueError(
                        f'Field "{key}": "{field}" has to be numeric'
                    )

        if 'min' in values and 'max' in values:
            if values['max'] < values['min']:
                raise ValueError(
                    f'Field "{key}": the "max" field has to be greater than "min" field'
                )

        if 'contains' in values and not isinstance(values['contains'], str):
            raise ValueError(
                f'Field "{key}": "contains" has to be a string'
            )

        if values['type'] == 'str':
            for field in values:
                if field in ['min', 'max']:
                    raise ValueError(
                        f'Field "{key}": unsupported field ("{field}") for "{values["type"]}" data'
                    )
