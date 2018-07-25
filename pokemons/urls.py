from django.urls import path
from pokemons import views

urlpatterns = [
    path('', views.Desktop.as_view(), name='desktop'),
    path('desktop/<int:pk>', views.Details.as_view(), name='details'),
    path('card/<int:pk>', views.Card.as_view(), name='card'),
    path('desktop/new_pokemon', views.NewPokemon.as_view(), name='new_pokemon'),
]
