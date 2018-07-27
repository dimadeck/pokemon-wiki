from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from pokemon_info import PokemonInfo
from pokemons.forms import StatisticForm, SpriteForm, AbilityForm, TypeForm
from pokemons.functions import set_dict
from pokemons.models import Pokemon, Statistic, Sprites, Type, Ability

PAGINATION_PAGES = 5


class Desktop(generic.ListView):
    template_name = "desktop.html"
    model = Pokemon
    context_object_name = "pokemons"
    queryset = Pokemon.objects.all()

    def get_queryset(self):
        queryset = super(Desktop, self).get_queryset()

        paginator = Paginator(queryset, PAGINATION_PAGES)
        page = self.request.GET.get('page')
        try:
            pokemons = paginator.page(page)
        except PageNotAnInteger:
            pokemons = paginator.page(1)
        except EmptyPage:
            pokemons = paginator.page(paginator.num_pages)
        return pokemons

    def get_context_data(self, object_list=None, **kwargs):
        context = super(Desktop, self).get_context_data()
        context['pokemons'] = self.get_queryset()
        return context


class Details(generic.DetailView):
    template_name = "details.html"
    model = Pokemon

    def get_object(self, queryset=None):
        obj = get_object_or_404(Pokemon, pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, object_list=None, **kwargs):
        context = super(Details, self).get_context_data()
        context['stats'] = get_object_or_404(Statistic, pk=self.get_object().stats.id)
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
        context['form2'] = StatisticForm(instance=get_object_or_404(Statistic, pk=self.get_object().stats.id))
        context['form3'] = SpriteForm(instance=get_object_or_404(Sprites, pk=self.get_object().sprites.id))
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        Statistic.objects.select_for_update().filter(pk=self.get_object().stats.id).update(
            **set_dict(form.data, StatisticForm.Meta.fields))
        Sprites.objects.select_for_update().filter(pk=self.get_object().sprites.id).update(
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


class SearchView(generic.ListView):
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        founded = Pokemon.objects.filter(Q(name__icontains=query))

        paginator = Paginator(founded, PAGINATION_PAGES)
        page = self.request.GET.get('page')
        try:
            founded = paginator.page(page)
        except PageNotAnInteger:
            founded = paginator.page(1)
        except EmptyPage:
            founded = paginator.page(paginator.num_pages)
        return founded

    def get_context_data(self, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data()
        query = self.request.GET.get('q')
        context['last_query'] = query
        context['pokemon_list'] = self.get_queryset()
        return context


class Add(generic.TemplateView):
    template_name = "add.html"

    def post(self, request, *args, **kwargs):
        try:
            pok = PokemonInfo(request.POST['add'])
            pok.collect_info()
            pd = pok.dictionary
            stat_obj = Statistic.objects.create(**set_dict(pd['pok_stats'], StatisticForm.Meta.fields))
            stat_obj.save()

            sprite_obj = Sprites.objects.create(**set_dict(pd['pok_sprites'], SpriteForm.Meta.fields))
            sprite_obj.save()

            other_fields = (
                'pok_name', 'pok_weight', 'pok_height', 'pok_color', 'pok_generation', 'pok_eggs', 'pok_gender')
            fields = ('name', 'weight', 'height', 'color', 'generation', 'eggs', 'gender')
            obj = Pokemon.objects.create(stats=stat_obj, sprites=sprite_obj, **set_dict(pd, fields, other_fields))
            obj.stats = stat_obj
            obj.sprites = sprite_obj
            obj.save()

            for type in pd['pok_types']:
                type_obj, created = Type.objects.get_or_create(ty_name=type)
                obj.types.add(type_obj)
                obj.save()

            for ability in pd['pok_abilities']:
                ability_obj, created = Ability.objects.get_or_create(ab_name=ability)
                obj.abilities.add(ability_obj)
                obj.save()
        except:
            pass
        return redirect(reverse_lazy('desktop'))
