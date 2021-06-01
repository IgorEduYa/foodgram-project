# Generated by Django 3.2.3 on 2021-06-01 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(verbose_name='Количество ингредиента')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('BF', 'Завтрак'), ('LC', 'Обед'), ('DN', 'Ужин')], default='BF', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('dimension', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='recipe_images/', verbose_name='Картинка')),
                ('text', models.TextField(help_text='Опишите здесь рецепт приготовления', verbose_name='Описание рецепта')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации рецепта')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
                ('components', models.ManyToManyField(related_name='meals', to='recipes.Component')),
                ('tag', models.ManyToManyField(related_name='category_recipe', to='recipes.Tag')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.AddField(
            model_name='component',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='component',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.unit'),
        ),
    ]