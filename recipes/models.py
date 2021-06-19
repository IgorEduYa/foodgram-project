from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Unit(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Component(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        related_name='ingredients',
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    value = models.IntegerField(verbose_name='Количество ингредиента')


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipe_images/',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите здесь рецепт приготовления'
    )
    components = models.ManyToManyField(
        Unit,
        through=Component,
        related_name='meals',
    )
    tag = models.ManyToManyField(
        'Tag',
        related_name='categories'
    )
    time = models.IntegerField(
        verbose_name='Время приготовления',
        default=30,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title[:20]


class Tag(models.Model):
    BREAKFAST = 'BF'
    LUNCH = 'LC'
    DINNER = 'DN'
    CHOICES = [
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (DINNER, 'Ужин'),
    ]
    name = models.CharField(
        max_length=2,
        choices=CHOICES,
        default=BREAKFAST,
        unique=True,
        verbose_name='Тэг',
    )

    def __str__(self):
        return self.name
