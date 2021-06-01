from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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
        'Component',
        related_name='meals',
    )
    tag = models.ManyToManyField(
        'Tag',
        related_name='category_recipe'
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
    )

    def __str__(self):
        return self.name


class Unit(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10)


class Component(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name='Количество ингредиента')
