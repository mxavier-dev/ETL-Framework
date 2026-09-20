import json
from src.transform.validator import validate_type
from src.transform.cleaner import remove_duplicates


class Transformer:
    def transform(self, lst):
        with open('schemas/user.json', 'r', encoding='utf-8') as arq:
            schema = json.load(arq)
            keys = list(schema.keys())

        lst_no_repeat = remove_duplicates(lst)

        for line in lst_no_repeat:
            for key in keys:
                match key:
                    case 'id':
                        if validate_type(line.get('id'), schema.get('id')['type']):
                            line['id'] = int(line['id'])
                        else:
                            line['id'] = None

                    case 'name':
                        if validate_type(line.get('name'), schema.get('name')['type']):
                            reject_caracters = '",.-_*\'+#!@~^()[]?|;:'
                            for carac in reject_caracters:
                                line['name'] = line['name'].replace(carac, '')

                    case 'age':
                        if validate_type(line.get('age'), schema.get('age')['type']):
                            line['age'] = int(line['age'])
                            if not (0 <= line['age'] <= 120):
                                line['age'] = None
                        else:
                            line['age'] = None


                    case 'email':
                        if validate_type(line.get('email'), schema.get('email')['type']):
                            if not any(i == "@" for i in line.get('email')):
                                line['email'] = None

                    case 'phone':
                        if validate_type(line.get('phone'), schema.get('phone')['type']):
                            if not any(i.isdigit() for i in line['phone']):
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
