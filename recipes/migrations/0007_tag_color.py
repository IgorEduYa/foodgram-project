# Generated by Django 3.2.3 on 2021-06-21 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20210621_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('orange', 'Orange'), ('green', 'Green'), ('purple', 'Purple')], default='orange', max_length=10, verbose_name='Color'),
        ),
    ]
