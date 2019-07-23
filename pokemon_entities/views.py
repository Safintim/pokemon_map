import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.all():
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, pokemon_entity.pokemon.image.path)

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else None,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(pk=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=requested_pokemon):
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, pokemon_entity.pokemon.image.path)

    pokemon = {
            'pokemon_id': requested_pokemon.id,
            'img_url': requested_pokemon.image.url if requested_pokemon.image else None,
            'description': requested_pokemon.description,
            'title_ru': requested_pokemon.title,
            'title_en': requested_pokemon.title_en,
            'title_jp': requested_pokemon.title_jp,
    }
    if requested_pokemon.next_evolution:
        pokemon['next_evolution'] = {
            'title_ru': requested_pokemon.next_evolution.title,
            'pokemon_id': requested_pokemon.next_evolution.id,
            'img_url': (requested_pokemon.next_evolution.image.url
                        if requested_pokemon.next_evolution.image else None),
        }
    print(requested_pokemon.previous_evolution)
    if requested_pokemon.previous_evolution:
        pokemon['previous_evolution'] = {
            'title_ru': requested_pokemon.previous_evolution.title,
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': (requested_pokemon.previous_evolution.image.url
                        if requested_pokemon.previous_evolution.image else None),
        }
    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
