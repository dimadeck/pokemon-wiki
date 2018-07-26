from django.db import models


class Sprites(models.Model):
    back_female = models.URLField(blank=True, null=True)
    back_shiny_female = models.URLField(blank=True, null=True)
    back_default = models.URLField(blank=True, null=True)
    front_female = models.URLField(blank=True, null=True)
    front_shiny_female = models.URLField(blank=True, null=True)
    back_shiny = models.URLField(blank=True, null=True)
    front_default = models.URLField(blank=True, null=True)
    front_shiny = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Спрайты"
        verbose_name_plural = "Спрайты"


class Type(models.Model):
    ty_name = models.CharField(max_length=20, verbose_name="Тип покемона", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Statistic(models.Model):
    speed = models.IntegerField(default=0, verbose_name="Скорость покемона")
    special_defense = models.IntegerField(default=0, verbose_name="Специальная защита покемона")
    special_attack = models.IntegerField(default=0, verbose_name="Специальная атака покемона")
    defense = models.IntegerField(default=0, verbose_name="Защита покемона")
    attack = models.IntegerField(default=0, verbose_name="Атака покемона")
    hp = models.IntegerField(default=0, verbose_name="Здоровье покемона")

    def __str__(self):
        score = self.special_attack + self.special_defense + self.speed + self.attack + self.defense
        return str(score)

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"


class Ability(models.Model):
    ab_name = models.CharField(max_length=20, verbose_name="Способность покемона", unique=True)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = "Способность"
        verbose_name_plural = "Способности"


class Pokemon(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя покемона", unique=True)
    weight = models.FloatField(default=0, verbose_name="Вес покемона")
    height = models.FloatField(default=0, verbose_name="Рост покемона")
    color = models.CharField(max_length=20, verbose_name="Цвет покемона")
    generation = models.CharField(max_length=20, verbose_name="Поколение покемона")
    eggs = models.CharField(max_length=20, verbose_name="Яйцо покемона")
    gender = models.CharField(max_length=20, verbose_name="Пол покемона")
    types = models.ManyToManyField(Type, null=True)
    abilities = models.ManyToManyField(Ability, null=True)
    stats = models.OneToOneField(Statistic, on_delete=models.CASCADE)
    sprites = models.OneToOneField(Sprites, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"
