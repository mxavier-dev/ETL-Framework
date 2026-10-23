import pytest

from src.transform.Transformer import Transformer

def test_valid_data_to_type_int():
    data = [{"age": '20'}]

    schema = {"age": {
        "type": "int"
    }}

    transformed_data = Transformer().transform(data, schema)
    assert isinstance(transformed_data[0]['age'], int)
    assert transformed_data[0]['age'] == 20

def test_invalid_data_int_to_none():
    data = [{"age": "abc"}]

    schema = {"age": {
        "type": "int"
    }}

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['age'] is None

def test_valid_data_to_type_float():
    data = [{'price': '20.5'}]
    schema = {'price': {
        'type': 'float'
    }}

    transformed_data = Transformer().transform(data, schema)
    assert isinstance(transformed_data[0]['price'], float)
    assert transformed_data[0]['price'] == 20.5

def test_invalid_data_float_to_none():
    data = [{"price": "abc"}]

    schema = {"price": {
        "type": "float"
    }}

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['price'] is None

@pytest.mark.parametrize('value, expected',
                         [
                             ('false', False),
                             ('False', False),
                             ('True', True),
                             ('true', True),
                         ])
def test_valid_data_to_type_bool(value, expected):
    data = [{'activate': value}]
    schema = {'activate': {
        'type': 'bool'
    }}

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['activate'] is expected

@pytest.mark.parametrize('value', ['falses', 'trues', 'abc', 24])
def test_invalid_data_bool_to_none(value):
    data = [{'activate': value}]
    schema = {'activate': {
        'type': 'bool'
    }}

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['activate'] is None

def test_valid_data_to_type_list():
    data = [{'data': [1,2,3]}]
    schema = {'data': {
        'type': 'list'
    }}

    transformed_data = Transformer().transform(data, schema)
    assert isinstance(transformed_data[0]['data'], list)

@pytest.mark.parametrize('values',
                         ((1,2,3), {'1': 2, '2': 3}, 1, 'xp', True))
def test_invalid_data_list_to_none(values):
    data = [{'data': values}]
    schema = {'data': {
        'type': 'list'
    }}

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['data'] is None

def test_valid_data_to_type_dict():
    data = [{'data': {'a': 2}}]
    schema = {'data': {
        'type': 'dict'
    }}


    transformed_data = Transformer().transform(data, schema)
    assert isinstance(transformed_data[0]['data'], dict)

@pytest.mark.parametrize('values',
                         ((1,2,3), [1,2,3], 1, 'xp', True))
def test_invalid_data_dict_to_none(values):
    data = [{'data': values}]
    schema = {'data': {
        'type': 'dict'
    }}


    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['data'] is None

def test_valid_data_to_type_tuple():
    data = [{'data': (1,'a',True)}]
    schema = {'data': {
        'type': 'tuple'
    }}

    transformed_data = Transformer().transform(data, schema)
    assert isinstance(transformed_data[0]['data'], tuple)

@pytest.mark.parametrize('values',
                         ({'a': 1, 'b': 2}, [1,2,3], 1, 'xp', True))
def test_invalid_data_tuple_to_none(values):
    data = [{'data': values}]
    schema = {'data': {
        'type': 'tuple'
    }}

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['data'] is None

@pytest.mark.parametrize('id,name,age',
                         [('two','jhon','abc'),
                          ('2', 50, '25'),
                          (2, 'jhon', 50)])
def test_structure_is_based_on_schema(id, name, age):
    data = [{'id': id,
            'name': name,
            'age': age,
            'phone': '2222-2222',
            'email': 'someone@email.com'
            }]
    schema = {
        'id': {
            'type': 'int'
        },
        'name': {
            'type': 'str'
        },
        'age': {
            'type': 'int'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert len(transformed_data[0]) == len(schema)
    assert list(transformed_data[0]) == list(schema)

@pytest.mark.parametrize('age',
                         [18,50,120])
def test_valid_min_max_values(age):
    data = [{'age': age}]
    schema = {
        'age': {
            'type': 'int',
            'min': 18,
            'max': 120
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['age'] == age

def test_value_below_min_returns_none():
    data = [{'age': 15}]
    schema = {
        'age': {
            'type': 'int',
            'min': 18
        }
    }

    transformed_data = Transformer().transform(data,schema)
    assert transformed_data[0]['age'] is None

def test_value_above_max_returns_none():
    data = [{'age': 200}]
    schema = {
        'age': {
            'type': 'int',
            'max': 120
        }
    }

    transformed_data = Transformer().transform(data,schema)
    assert transformed_data[0]['age'] is None

def test_remove_duplicates_data_int_types():
    data = [
        {'data1': 1},
        {'data1': 2},
        {'data1': 1}
    ]
    schema = {
        'data1': {
            'type': 'int'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert len(transformed_data) == 2

def test_remove_duplicates_data_string_types():
    data = [
        {'data1': 'string'},
        {'data1': 'strings'},
        {'data1': 'string'}
    ]
    schema = {
        'data1': {
            'type': 'str'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert len(transformed_data) == 2

def test_remove_duplicates_data_list_types():
    data = [
        {'data1': [1,3,2]},
        {'data1': [1,2,3]},
        {'data1': [1,2,3]}
    ]
    schema = {
        'data1': {
            'type': 'list'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert len(transformed_data) == 2

def test_remove_duplicates_data_dict_type():
    data = [
        {'data1': {'a': 1, 'b': 2}},
        {'data1': {'c': 3, 'd': 4}},
        {'data1': {'a': 1, 'b': 2}}
    ]
    schema = {
        'data1': {
            'type': 'dict'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert len(transformed_data) == 2

@pytest.mark.parametrize('id,name,age, expected',
                         ((5,'j',25, (5,'j', 25)),
                          ('abc', 25, 'five', (None, '25', None))))
def test_quantity_data_preservation_even_in_invalid_data(id,name,age, expected):
    data = [
        {
        'id': id,
        'name': name,
        'age': age
        }
    ]
    schema = {
        'id': {
            'type': 'int'
        },
        'name': {
            'type': 'str'
        },
        'age': {
            'type': 'int'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert len(transformed_data[0]) == 3
    assert tuple(transformed_data[0].values()) == expected

def test_data_preservation():
    data = [
        {
        'id': '2',
        'name': 14,
        'age': '19'
        }
    ]
    schema = {
        'id': {
            'type': 'int'
        },
        'name': {
            'type': 'str'
        },
        'age': {
            'type': 'int'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['id'] == 2
    assert transformed_data[0]['name'] == '14'
    assert transformed_data[0]['age'] == 19

def test_valid_extract_of_values_nestled():
    data = [
        {'address': {'street': 'SomeStreet',
                    'city': 'Florida'}}
    ]
    schema = {
        'address': {
            'type': 'str',
            'source': 'address.city'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['address'] == 'Florida'

def test_invalid_field_for_extract_values_nestled():
    data = [
        {'address': {'street': 'SomeStreet',
                    'city': 'Florida'}}
    ]
    schema = {
        'address': {
            'type': 'str',
            'source': 'address.country'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['address'] is None

def test_invalid_first_data_for_extract_values_nestled():
    data = [
        {'address': {'street': 'SomeStreet',
                    'city': 'Florida'}}
    ]
    schema = {
        'address': {
            'type': 'str',
            'source': 'country.city'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['address'] is None

def test_invalid_unexpected_type_data_for_extract_values_nestled():
    data = [
        {'address': 'Florida'}
    ]
    schema = {
        'address': {
            'type': 'str',
            'source': 'address.city'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['address'] is None

def test_remove_duplicates_is_true():
    data = [
        {'id': 1},
        {'id': 1},
        {'id': 2}
    ]
    schema = {
        'id': {
            'type': 'int'
        }
    }

    transformed_data = Transformer().transform(data, schema, remove_duplicate=True)
    assert len(transformed_data) == 2

def test_remove_duplicates_is_false():
    data = [
        {'id': 1},
        {'id': 1},
        {'id': 2}
    ]
    schema = {
        'id': {
            'type': 'int'
        }
    }

    transformed_data = Transformer().transform(data, schema, remove_duplicate=False)
    assert len(transformed_data) == 3

def test_remove_duplicates_by_default():
    data = [
        {'id': 1},
        {'id': 1},
        {'id': 2}
    ]
    schema = {
        'id': {
            'type': 'int'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert len(transformed_data) == 2

def test_clean_true_valid_transform_clean_name():
    data = [
        {
            'name': 'Jo@a.,h'
        }
    ]
    schema = {
        'name': {
            'type': 'str',
            'clean': True,
            'transform': 'clean_name'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['name'] == 'Joah'

def test_clean_true_valid_transform_clean_phone():
    data = [
        {
            'phone': '11 9999-@%$@!$9999;.,'
        }
    ]
    schema = {
        'phone': {
            'type': 'str',
            'clean': True,
            'transform': 'clean_phone'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['phone'] == '11 99999999'

def test_valid_data_with_contains_field_return_data():
    data = [
        {
            'email': 'email@email.com'
        }
    ]
    schema = {
        'email': {
            'type': 'str',
            'contains': '@'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['email'] == 'email@email.com'

def test_invalid_data_with_contains_field_return_none():
    data = [
        {
            'email': 'email.email.com'
        }
    ]
    schema = {
        'email': {
            'type': 'str',
            'contains': '@'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['email'] is None

def test_clean_transform_with_contains_field_return_clean_data():
    data = [
        {
            'name': 'M@at$$h.,'
        }
    ]
    schema = {
        'name': {
            'type': 'str',
            'clean': True,
            'transform': 'clean_name',
            'contains': 'M'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['name'] == 'Math'

def test_clean_transform_with_contains_field_return_none():
    data = [
        {
            'name': 'M@at$$h.,'
        }
    ]
    schema = {
        'name': {
            'type': 'str',
            'clean': True,
            'transform': 'clean_name',
            'contains': '@'
        }
    }

    transformed_data = Transformer().transform(data, schema)
    assert transformed_data[0]['name'] is None
