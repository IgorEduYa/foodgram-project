# Generated by Django 3.2.3 on 2021-06-06 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210604_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='time',
            field=models.IntegerField(default=30, verbose_name='Время приготовления'),
        ),
    ]
