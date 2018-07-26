def set_dict(data, fields):
    dictionary = {}
    for field in fields:
        dictionary[field] = data[field]
    return dictionary