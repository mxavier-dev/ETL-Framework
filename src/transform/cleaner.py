def remove_duplicates(data :list[dict]) -> list[dict]:
    viewed_values = set()
    lst_no_repeat = [
                d for d in data
                if tuple(d.items()) not in viewed_values and
                not viewed_values.add(tuple(d.items()))
              ]

    # and not isinstance(d, (list, tuple, dict))
    return lst_no_repeat

def clean_phone(data):
    if any(i.isdigit() for i in data):
      reject_carac = '\'\";;,./?!@#$%-.+[](){*}/'
      for carac in reject_carac:
        data = data.replace(carac, '')
      return data
    else:
        return None

def clean_name(data):
    reject_carac = '\'\";;,./?!@#$%.+[](){*}/'
    for carac in reject_carac:
      data = data.replace(carac, '')
    return data

transformations = {
   'clean_name': clean_name,
   'clean_phone': clean_phone
}
