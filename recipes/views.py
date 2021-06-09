from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Recipe, User


def index(request, tag=None):
    if tag:
        recipes = Recipe.objects.filter(tag__name=str(tag))
    else:
        recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
         request,
         'index.html',
         {'page': page, 'paginator': paginator}
    )


def profile(request, username, tag=None):
    author = get_object_or_404(User, username=username)
    if tag:
        recipes = author.recipes.filter(tag__name=str(tag))
    else:
        recipes = author.recipes.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'profile.html',
        {
            'page': page,
            'paginator': paginator,
            'author': author,
        }
    )


def recipe_view(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_page.html', {'recipe': recipe,})
