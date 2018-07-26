from django.contrib import admin

import pokemons.models as pokemons

admin.site.register(pokemons.Pokemon)
admin.site.register(pokemons.Ability)
admin.site.register(pokemons.Type)
admin.site.register(pokemons.Sprites)
admin.site.register(pokemons.Statistic)
