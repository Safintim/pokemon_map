from django.db import models


class Pokemon(models.Model):
    title = models.CharField('Имя на русском', max_length=100)
    title_en = models.CharField('Имя на англ', max_length=100, blank=True)
    title_jp = models.CharField('Имя на японском', max_length=100, blank=True)
    image = models.ImageField('Изображение', upload_to='pokemons', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    previous_evolution = models.ForeignKey('Pokemon',
                                           verbose_name='Из кого эволюционировал',
                                           related_name='prev_evo',
                                           on_delete=models.SET_NULL,
                                           null=True)
    next_evolution = models.ForeignKey('Pokemon',
                                       verbose_name='В кого эволюционирует',
                                       related_name='next_evo',
                                       on_delete=models.SET_NULL,
                                       null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления')
    disappeared_at = models.DateTimeField('Время исчезновения')
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Жизни', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return self.pokemon.title
