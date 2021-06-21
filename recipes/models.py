from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Unit(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

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
    value = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        validators=[MinValueValidator(
            limit_value=1,
            message='Количество ингредиента меньше единицы!',
        )],
    )

    class Meta:
        verbose_name = 'Ингредиент для блюда'
        verbose_name_plural = 'Ингредиенты для блюда'


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
    time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        default=30,
        validators=[MinValueValidator(
            limit_value=1,
            message='Время приготовления меньше 1 минуты!',
        )],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title[:20]


class Tag(models.Model):
    class Colors(models.TextChoices):
        ORANGE = 'orange'
        GREEN = 'green'
        PURPLE = 'purple'

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
    slug = models.SlugField(unique=True)
    color = models.CharField(
        max_length=10,
        verbose_name='Color',
        choices=Colors.choices,
        default=Colors.ORANGE,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name

    def readable_name(self):
        return dict(Tag.CHOICES)[self.name]
