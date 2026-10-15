def remove_duplicates(data: list[dict]) -> list[dict]:
  lst_no_repeat, viewed_data = [], []
  for line in data:
    if line in viewed_data:
       continue
    viewed_data.append(line)
    lst_no_repeat.append(line)

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

TRANSFORMATIONS = {
   'clean_name': clean_name,
   'clean_phone': clean_phone
}
