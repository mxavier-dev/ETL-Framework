import json

def validate_data(lst):
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
                    if not line['id'].isnumeric():
                        line['id'] = None

                case 'name':
                    if line['name'] == '':
                        line['name'] = None
                    else:
                        rejected_carac = ['"', '.', ',', '_', '-', '+', '=', '(', ')', '&']
                        for carac in rejected_carac:
                            line['name'] = line['name'].replace(carac, '')
                case 'age':
                    if not line['age'].isnumeric():
                        line['age'] = None
                    else:
                        line['age'] = int(line['age'])
                        if line['age'] > 120 or line['age'] < 0:
                            line['age'] = None

                case 'email':
                    if not any(i == '@' for i in line['email']):
                        line['email'] = None

                case 'phone':
                    if not any(i.isnumeric() for i in line['phone']):
                        line['phone'] = None

                case 'city':
                    if line['city'] == '':
                        line['city'] = None
                case _:
                    raise ValueError('')

    return lst_no_repeat
