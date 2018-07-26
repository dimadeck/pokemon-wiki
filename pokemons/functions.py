def set_dict(data, fields, other_fields=None):
    dictionary = {}
    if other_fields is None:
        other_fields = fields
    for num in range(len(fields)):
        dictionary[fields[num]] = data[other_fields[num]]
    return dictionary
