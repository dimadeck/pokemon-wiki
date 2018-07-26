from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from pokemons.models import Pokemon, Statistic, Sprites, Type, Ability
from pokemons.forms import StatisticForm, SpriteForm, AbilityForm, TypeForm
from pokemons.functions import set_dict


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
        'name', 'weight', 'height', 'color', 'generation', 'eggs', 'gender')  # , 'types', 'abilities')

    def get_context_data(self, **kwargs):
        context = super(NewPokemon, self).get_context_data(**kwargs)
        context['form2'] = StatisticForm
        context['form3'] = SpriteForm
        context['ability_form'] = AbilityForm
        context['type_form'] = TypeForm
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        stat_obj = Statistic.objects.create(**set_dict(form.data, StatisticForm.Meta.fields))
        stat_obj.save()

        sprite_obj = Sprites.objects.create(**set_dict(form.data, SpriteForm.Meta.fields))
        sprite_obj.save()

        type_obj, created = Type.objects.get_or_create(ty_name=form.data['ty_name'])
        ability_obj, created = Ability.objects.get_or_create(ab_name=form.data['ab_name'])

        obj.stats = stat_obj
        obj.sprites = sprite_obj
        obj.save()

        obj.types.add(type_obj)
        obj.abilities.add(ability_obj)
        obj.save()

        return redirect(reverse_lazy('desktop'))


class EditPokemon(generic.UpdateView):
    template_name = "edit_pokemon.html"
    model = Pokemon
    fields = ('name', 'weight', 'height', 'color', 'generation', 'eggs', 'gender', 'types', 'abilities')
    success_url = reverse_lazy('desktop')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Pokemon, pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(EditPokemon, self).get_context_data(**kwargs)
        context['form2'] = StatisticForm(instance=get_object_or_404(Statistic, pk=self.kwargs['pk']))
        context['form3'] = SpriteForm(instance=get_object_or_404(Sprites, pk=self.kwargs['pk']))
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        Statistic.objects.select_for_update().filter(pk=self.kwargs['pk']).update(
            **set_dict(form.data, StatisticForm.Meta.fields))
        Sprites.objects.select_for_update().filter(pk=self.kwargs['pk']).update(
            **set_dict(form.data, SpriteForm.Meta.fields))

        obj.abilities.clear()
        obj.types.clear()
        obj.save()

        for type in form.fields['types'].queryset:
            obj.types.add(type)
            obj.save()
        for ability in form.fields['abilities'].queryset:
            obj.abilities.add(ability)
            obj.save()
        return redirect(reverse_lazy('desktop'))


class DeletePokemon(generic.DeleteView):
    template_name = "delete.html"
    model = Pokemon
    success_url = reverse_lazy('desktop')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Pokemon, pk=self.kwargs['pk'])
        return obj
