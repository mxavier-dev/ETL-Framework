import pytest

from src.config.schema_validator import validate_schema

@pytest.fixture
def valid_schema():
    schema = {
        "id": {
            "type": "int",
            "source": "id"
        },
        "name": {
            "type": "str",
            "source": "name",
            "clean": True,
            "transform": "clean_name"
        },
        "age": {
            "type": "int",
            "source": "age",
            "min": 0,
            "max": 120
        },
        "city": {
            "type": "str",
            "source": "address.city",
            "contains": '.'
        }
    }
    return schema

def test_valid_schema(valid_schema):
    validate_schema(valid_schema)

def test_unsupported_field(valid_schema):
    schema = valid_schema
    schema['id']['unsuport'] = True

    with pytest.raises(ValueError, match='Unsupported field'):
        validate_schema(schema)

def test_type_field_missing(valid_schema):
    schema = valid_schema
    del schema['id']['type']

    with pytest.raises(ValueError, match='"type" field has to exist'):
        validate_schema(schema)

def test_unsupported_type_data(valid_schema):
    schema = valid_schema
    schema['id']['type'] = 'date'

    with pytest.raises(ValueError, match='Unsupported type'):
        validate_schema(schema)

def test_clean_is_not_boolean(valid_schema):
    schema = valid_schema
    schema['name']['clean'] = 'something'

    with pytest.raises(ValueError, match='"clean" has to be a boolean'):
        validate_schema(schema)

def test_clean_is_true_but_transform_is_missing(valid_schema):
    schema = valid_schema
    del schema['name']['transform']

    with pytest.raises(ValueError, match='requires a "transform"'):
        validate_schema(schema)

def test_clean_is_false_with_no_transform(valid_schema):
    schema = valid_schema
    schema['name']['clean'] = False
    del schema['name']['transform']

    validate_schema(schema)

def test_transform_not_missing_and_clean_is_false(valid_schema):
    schema = valid_schema
    schema['name']['clean'] = False

    with pytest.raises(ValueError, match='requires "clean": true'):
        validate_schema(schema)

def test_unsupported_transform(valid_schema):
    schema = valid_schema
    schema['name']['transform'] = 'something'

    with pytest.raises(ValueError, match='unsupported transform'):
        validate_schema(schema)

@pytest.mark.parametrize('field', ('min', 'max'))
def test_min_or_max_fields_is_not_integer_when_type_is_int(field, valid_schema):
    schema = valid_schema
    schema['age']['type'] = 'int'
    schema['age'][field] = 'two'

    with pytest.raises(ValueError, match='has to be an integer'):
        validate_schema(schema)

@pytest.mark.parametrize('field', ('min', 'max'))
@pytest.mark.parametrize('value', (0, 10, -5))
def test_valid_min_or_max_values_int_type(value, field, valid_schema):
    schema = valid_schema
    del schema['age']['min']
    del schema['age']['max']
    schema['age'][field] = value

    validate_schema(schema)

@pytest.mark.parametrize('field', ('min', 'max'))
def test_min_or_max_fields_is_not_numeric_or_int_when_type_is_float(field, valid_schema):
    schema = valid_schema
    schema['age']['type'] = 'float'
    schema['age'][field] = 'two.two'

    with pytest.raises(ValueError, match='has to be numeric'):
        validate_schema(schema)

@pytest.mark.parametrize('field', ('min', 'max'))
@pytest.mark.parametrize('value', (0, 10, -5.2, 10.5))
def test_valid_min_or_max_values_float_type(value, field, valid_schema):
    schema = valid_schema
    schema['age']['type'] = 'float'
    del schema['age']['min']
    del schema['age']['max']
    schema['age'][field] = value

    validate_schema(schema)

def test_min_field_is_greater_than_max_field(valid_schema):
    schema = valid_schema
    schema['age']['min'] = 125

    with pytest.raises(ValueError, match='the "max" field has to be greater'):
        validate_schema(schema)

def test_contains_field_when_type_is_not_string(valid_schema):
    schema = valid_schema
    schema['city']['type'] = 'float'

    with pytest.raises(ValueError, match='only supported for string fields'):
        validate_schema(schema)

def test_contains_is_not_a_string(valid_schema):
    schema = valid_schema
    schema['city']['contains'] = 1

    with pytest.raises(ValueError, match='"contains" has to be a string'):
        validate_schema(schema)

@pytest.mark.parametrize('field', ('min', 'max'))
def test_min_or_max_fields_in_a_string_type_key(field, valid_schema):
    schema = valid_schema
    del schema['age'][field]
    schema['age']['type'] = 'string'

    with pytest.raises(ValueError, match='for string data'):
        validate_schema(schema)

def test_min_max_fields_equal_values(valid_schema):
    schema = valid_schema
    schema['age']['min'] = 10
    schema['age']['max'] = 10

    validate_schema(schema)

def test_min_max_fields_valid_values(valid_schema):
    schema = valid_schema
    schema['age']['min'] = 10
    schema['age']['max'] = 120

    validate_schema(schema)
