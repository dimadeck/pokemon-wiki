import pokebase as pb


class PokemonInfo:
    def __init__(self, pok_ID):
        self.pokemon = pb.pokemon(pok_ID)
        self.dictionary = {}

    def get_id(self):
        return self.pokemon.id

    def get_name(self):
        return self.pokemon.name

    def get_types(self):
        pok_types = []
        for pok_type in self.pokemon.types:
            pok_types.append(pok_type.type.name)
        return pok_types

    def get_abilities(self):
        pok_abilities = []
        for ability in self.pokemon.abilities:
            is_hidden = '(*)' if ability.is_hidden else ''
            pok_abilities.append(f'{ability.ability.name}{is_hidden}')
        return pok_abilities

    def get_sprites(self):
        pok_sprites = {}
        pok_sprites['back_female'] = self.pokemon.sprites.back_female
        pok_sprites['back_shiny_female'] = self.pokemon.sprites.back_shiny_female
        pok_sprites['back_default'] = self.pokemon.sprites.back_default
        pok_sprites['front_female'] = self.pokemon.sprites.front_female
        pok_sprites['front_shiny_female'] = self.pokemon.sprites.front_shiny_female
        pok_sprites['back_shiny'] = self.pokemon.sprites.back_shiny
        pok_sprites['front_default'] = self.pokemon.sprites.front_default
        pok_sprites['front_shiny'] = self.pokemon.sprites.front_shiny
        return pok_sprites

    def get_generations(self):
        try:
            return pb.generation(self.pokemon.id).name
        except:
            return 'unknown'

    def get_gender(self):
        try:
            return pb.gender(self.pokemon.id).name
        except:
            return 'unknown'

    def get_weight(self):
        return self.pokemon.weight

    def get_height(self):
        return self.pokemon.height

    def get_color(self):
        try:
            return pb.pokemon_color(self.pokemon.id).name
        except:
            return 'unknown'

    def get_eggs(self):
        try:
            return pb.egg_group(self.pokemon.id).name
        except:
            return 'unknown'

    def get_stats(self):
        pok_stats = {}
        for stat in self.pokemon.stats:
            name = stat.stat.name.replace('-', '_')
            pok_stats[name] = stat.base_stat
        return pok_stats

    def collect_info(self):
        self.dictionary['pok_id'] = self.get_id()
        self.dictionary['pok_name'] = self.get_name()
        self.dictionary['pok_types'] = self.get_types()
        self.dictionary['pok_abilities'] = self.get_abilities()
        self.dictionary['pok_generation'] = self.get_generations()
        self.dictionary['pok_gender'] = self.get_gender()
        self.dictionary['pok_weight'] = self.get_weight()
        self.dictionary['pok_height'] = self.get_height()
        self.dictionary['pok_color'] = self.get_color()
        self.dictionary['pok_eggs'] = self.get_eggs()
        self.dictionary['pok_stats'] = self.get_stats()
        self.dictionary['pok_sprites'] = self.get_sprites()
