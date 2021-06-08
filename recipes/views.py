from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Recipe


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
