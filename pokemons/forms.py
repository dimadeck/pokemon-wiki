from django import forms

from pokemons.models import Pokemon, Statistic, Sprites, Ability, Type


class AbilityForm(forms.ModelForm):
    class Meta:
        model = Ability
        fields = ('ab_name',)


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ('ty_name',)


class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ('name', 'weight', 'height', 'color', 'generation', 'eggs',
                  'gender', 'types', 'abilities', 'stats', 'sprites')


class StatisticForm(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = ('speed', 'attack', 'special_attack', 'defense', 'special_defense', 'hp')


class SpriteForm(forms.ModelForm):
    class Meta:
        model = Sprites
        fields = ('back_female', 'back_shiny_female', 'back_default', 'back_shiny', 'front_female',
                  'front_shiny_female', 'front_default', 'front_shiny')
