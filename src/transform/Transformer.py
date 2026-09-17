import json
from src.transform.validator import validate_type

class Transformer:
    def transform(self, lst):
        with open('schemas/user.json', 'r', encoding='utf-8') as arq:
            schema = json.load(arq)
            keys = list(schema.keys())

        viewed_values = set()
        lst_no_repeat = [
                d for d in lst
                if tuple(d.items()) not in viewed_values and
                not viewed_values.add(tuple(d.items()))
              ]

        for line in lst_no_repeat:
            for key in keys:
                match key:
                    case 'id':
                        if line['id'].isdigit():
                            if not validate_type(int(line['id']), schema.get('id')['type']):
                                line['id'] = None
                        else:
                            line['id'] = None

                    case 'name':
                        if validate_type(line['name'], schema.get('name')['type']):
                            reject_caracters = '",.-_*\'+#!@~^()[]?|;:'
                            for carac in reject_caracters:
                                line['name'] = line['name'].replace(carac, '')
                        else:
                            line['name'] = None

                    case 'age':
                        if line['age'].isdigit():
                            line['age'] = int(line['age'])
                            if not (0 <= line['age'] <= 120):
                                line['age'] = None
                        else:
                            line['age'] = None

                    case 'email':
                        if (not validate_type(line['email'], schema.get('email')['type']) or
                        not any(i == "@" for i in line['email'])):
                            line['email'] = None

                    case 'phone':
                        if (not validate_type(line['phone'], schema.get('phone')['type']) or
                        not any(i.isdigit() for i in line['phone'])):
                            line['phone'] = None
                        else:
                            reject_caracters = '"([\{\}])/*-+.,:; '
                            for carac in reject_caracters:
                                line['phone'] = line['phone'].replace(carac, '')

                    case 'city':
                        if not validate_type(line['city'], schema.get('city')['type']):
                            line['city'] = None
                    case _:
                        continue

        return lst_no_repeat
