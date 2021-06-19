from django import template

from recipes.models import Recipe

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def check_favor(obj, user):
    favors = user.favoriters.all()
    recipes = Recipe.objects.filter(id__in=favors.values('recipe_id'))
    return obj in recipes


@register.filter
def check_purchase(obj, user):
    purchases = user.buyers.all()
    recipes = Recipe.objects.filter(id__in=purchases.values('recipe_id'))
    return obj in recipes
