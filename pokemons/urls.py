from django.urls import path
from pokemons import views

urlpatterns = [
    path('', views.Desktop.as_view(), name='desktop')]
