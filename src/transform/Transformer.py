from src.transform.validator import convert_value
from src.transform.cleaner import remove_duplicates, TRANSFORMATIONS

def get_nested_value(data: dict, path: str) -> object | None:
        value = data

        for key in path.split('.'):
            if not isinstance(value, dict):
                return None

            value = value.get(key)

            if value is None:
                return None

        return value

class Transformer:
    def transform(
            self,
            data: list[dict],
            schema: dict,
            remove_duplicate: bool | None = None
    ) -> list[dict]:

        new_lst = []
        for line in data:
            transformed_line = {}
            for field, config in schema.items():
                source = config.get('source', field)
                value_type = config['type']
                value = convert_value(get_nested_value(line, source), value_type)

                if value is None:
                    transformed_line[field] = None
                    continue

                if value_type in ["int", "float"]:
                    if 'min' in config and value < config['min']:
                        transformed_line[field] = None
                    elif 'max' in config and value > config['max']:
                        transformed_line[field] = None
                    else:
                        transformed_line[field] = value
                else:
                    transformed_line[field] = value

                    if config.get('clean'):
                        transform = TRANSFORMATIONS.get(config['transform'])
                        transformed_line[field] = transform(value)

                    if 'contains' in config:
                        if not config.get('contains') in transformed_line[field]:
                            transformed_line[field] = None

            new_lst.append(transformed_line)

        if remove_duplicate is False:
            return new_lst
        else:
            return remove_duplicates(new_lst)
