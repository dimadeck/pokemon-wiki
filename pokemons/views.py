from django.views import generic

from pokemons.models import Pokemon


class Desktop(generic.ListView):
    template_name = "desktop.html"
    model = Pokemon
    context_object_name = "pokemons"
    queryset = Pokemon.objects.all()

