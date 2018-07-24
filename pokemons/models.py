from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=20, verbose_name="Тип покемона", unique=True)


class Ability(models.Model):
    name = models.CharField(max_length=20, verbose_name="Способность покемона", unique=True)


class Statistic(models.Model):
    speed = models.IntegerField(default=0, verbose_name="Скорость покемона")
    special_defense = models.IntegerField(default=0, verbose_name="Специальная защита покемона")
    special_attack = models.IntegerField(default=0, verbose_name="Специальная атака покемона")
    defense = models.IntegerField(default=0, verbose_name="Защита покемона")
    attack = models.IntegerField(default=0, verbose_name="Атака покемона")
    hp = models.IntegerField(default=0, verbose_name="Здоровье покемона")


class Sprites(models.Model):
    back_female = models.URLField(blank=True)
    back_shiny_female = models.URLField(blank=True)
    back_default = models.URLField(blank=True)
    front_female = models.URLField(blank=True)
    front_shiny_femail = models.URLField(blank=True)
    back_shiny = models.URLField(blank=True)
    front_default = models.URLField(blank=True)
    front_shiny = models.URLField(blank=True)


class Pokemon(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя покемона", unique=True)
    weight = models.FloatField(default=0, verbose_name="Вес покемона")
    height = models.FloatField(default=0, verbose_name="Рост покемона")
    color = models.FloatField(default=0, verbose_name="Цвет покемона")
    generation = models.CharField(max_length=20, verbose_name="Поколение покемона")
    eggs = models.CharField(max_length=20, verbose_name="Яйцо покемона")
    gender = models.CharField(max_length=20, verbose_name="Пол покемона")
    types = models.ManyToManyField(Type)
    abilities = models.ManyToManyField(Ability)
    stats = models.OneToOneField(Statistic, on_delete=models.CASCADE)
    sprites = models.OneToOneField(Sprites, on_delete=models.CASCADE)
