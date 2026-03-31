from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Имя на русском')
    title_en = models.CharField(max_length=200, default='', blank=True, verbose_name='Имя на английском')
    title_jp = models.CharField(max_length=200, default='', blank=True, verbose_name='Имя на японском')
    picture = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', blank=True)
    previous_evolution = models.ForeignKey('self', verbose_name='Из кого эволюционирует', null=True, blank=True, related_name='next_evolutions', on_delete=models.SET_NULL)
    
    
    def __str__(self):
        return f'{self.title_ru}'

class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name='Покемон')
	lat = models.FloatField(verbose_name='Широта', null=True, blank=True)
	lon = models.FloatField(verbose_name='Долгота', null=True, blank=True)
	appeared_at = models.DateTimeField(verbose_name='Время появления', blank=True, null=True)
	disappeared_at = models.DateTimeField(verbose_name='Время исчезновения', blank=True, null=True)
	level = models.IntegerField(null=True, verbose_name='Уровень', blank=True)
	health = models.IntegerField(null=True, verbose_name='Здоровье', blank=True)
	strength = models.IntegerField(null=True, verbose_name='Сила', blank=True)
	defence = models.IntegerField(null=True, verbose_name='Защита', blank=True)
	