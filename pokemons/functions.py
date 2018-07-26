def set_dict(data, fields):
    dictionary = {}
    for field in fields:
        dictionary[field] = data[field]
    return dictionary


# fields = ['speed', 'attack', 'special_attack', 'defense', 'special_defense', 'hp']
# data = {'speed': 10, 'attack': 20, 'special_attack': 30, 'defense': 40, 'special_defense': 50, 'hp': 60}
# print(set_dict(data, fields))