from django.db import models 
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon
from .models import PokemonEntity


all_pokemons = PokemonEntity.objects.all()
print('all_pokemons')