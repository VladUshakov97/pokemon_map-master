import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon
from .models import PokemonEntity
from django.utils.timezone import localtime



MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    
    current_time = localtime()
    pokemons = PokemonEntity.objects.filter(disappeared_at__gte=current_time, appeared_at__lte=current_time)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        add_pokemon(
            folium_map, 
            pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.picture.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.picture.url),
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_on_map = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.picture.url),
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description
        }                                                    
    
    requested_pokemon = pokemon.entities.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon:
        add_pokemon(
            folium_map, 
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.picture.url)
        )
        
    
    if pokemon.previous_evolution:
        previous = {
        'title_ru': pokemon.previous_evolution.title_ru,
        'pokemon_id': pokemon.previous_evolution.id,
        'img_url': request.build_absolute_uri(pokemon.previous_evolution.picture.url)
        }
    else:
        previous = None

    next_pokemon = pokemon.next_evolutions.first()
    if next_pokemon:
        next_evolution = {
            'title_ru': next_pokemon.title_ru,
            'pokemon_id': next_pokemon.id,
            'img_url': request.build_absolute_uri(next_pokemon.picture.url),
            }
    else:
        next_evolution = None


    pokemon_on_map['previous_evolution'] = previous
    pokemon_on_map['next_evolution'] = next_evolution
     

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_map
    })
  