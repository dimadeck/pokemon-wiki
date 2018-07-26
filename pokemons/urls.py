from django.urls import path
from pokemons import views

urlpatterns = [
    path('', views.Desktop.as_view(), name='desktop'),
    path('desktop/<int:pk>', views.Details.as_view(), name='details'),
    path('card/<int:pk>', views.Card.as_view(), name='card'),
    path('desktop/new_pokemon', views.NewPokemon.as_view(), name='new_pokemon'),
    path('desktop/<int:pk>/edit_pokemon', views.EditPokemon.as_view(), name='edit_pokemon'),
    path('desktop/<int:pk>/delete', views.DeletePokemon.as_view(), name='delete_pokemon'),
    path('search', views.SearchView.as_view(), name='search'),
    path('add/<int:pk>', views.PokemonAddFromAPI.as_view(), name='add_pokemon')
]
