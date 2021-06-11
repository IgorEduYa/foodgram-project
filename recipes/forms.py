from django.forms import ModelForm
from .models import Recipe
from django import forms


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
