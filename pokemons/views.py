from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from pokemons.models import Pokemon, Statistic, Sprites
from pokemons.forms import StatisticForm, SpriteForm


class Desktop(generic.ListView):
    template_name = "desktop.html"
    model = Pokemon
    context_object_name = "pokemons"
    queryset = Pokemon.objects.all()


class Details(generic.DetailView):
    template_name = "details.html"
    model = Pokemon

    def get_object(self, queryset=None):
        obj = get_object_or_404(Pokemon, pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, object_list=None, **kwargs):
        context = super(Details, self).get_context_data()
        context['stats'] = get_object_or_404(Statistic, pk=self.kwargs['pk'])
        return context


class Card(generic.DetailView):
    template_name = "card.html"
    model = Pokemon

    def get_object(self, queryset=None):
        obj = get_object_or_404(Pokemon, pk=self.kwargs['pk'])
        return obj


class NewPokemon(generic.CreateView):
    template_name = "new_pokemon.html"
    model = Pokemon
    fields = (
        'name', 'weight', 'height', 'color', 'generation', 'eggs', 'gender', 'types',
        'abilities')

    def get_context_data(self, **kwargs):
        context = super(NewPokemon, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = StatisticForm
        if 'form3' not in context:
            context['form3'] = SpriteForm
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        stat_obj = Statistic.objects.create(
            speed=form.data['speed'],
            attack=form.data['attack'],
            special_attack=form.data['special_attack'],
            defense=form.data['defense'],
            special_defense=form.data['special_defense'],
            hp=form.data['hp'])
        stat_obj.save()

        sprite_obj = Sprites.objects.create(
            back_female=form.data['back_female'],
            back_shiny_female=form.data['back_shiny_female'],
            back_default=form.data['back_default'],
            back_shiny=form.data['back_shiny'],
            front_female=form.data['front_female'],
            front_shiny_female=form.data['front_shiny_female'],
            front_default=form.data['front_default'],
            front_shiny=form.data['front_shiny'])
        sprite_obj.save()

        obj.stats = stat_obj
        obj.sprites = sprite_obj
        obj.save()

        for type in form.data['types']:
            obj.types.add(type)
            obj.save()
        for ability in form.data['abilities']:
            obj.abilities.add(ability)
            obj.save()

        return redirect(reverse_lazy('desktop'))
