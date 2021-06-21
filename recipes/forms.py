from django import forms
from django.forms import ModelForm

from .models import Recipe, Tag


class RecipeForm(ModelForm):
    time = forms.IntegerField(min_value=1)
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'time', 'text', 'image']
