from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def check_favor(obj, user):
    favors = user.favoriters.all()
    recipes = []
    for favor in favors:
        recipes.append(favor.recipe)
    return obj in recipes
