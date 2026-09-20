def remove_duplicates(data :list[dict]) -> list[dict]:
    viewed_values = set()
    lst_no_repeat = [
                d for d in data
                if tuple(d.items()) not in viewed_values and
                not viewed_values.add(tuple(d.items()))
              ]

    # and not isinstance(d, (list, tuple, dict))
    return lst_no_repeat
