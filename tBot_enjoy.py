def founder(data, key):
    if key in data:
        return data[key]
    else:
        for value in data.values():
            if type(value) == dict:
                dict_lower = founder(value, key)
                if dict_lower is not None:
                    return dict_lower
        