from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from excel_response import ExcelResponse

from .forms import RecipeForm
from .models import Component, Recipe, Tag, Unit, User


def get_recipes(request, username=None):
    tag = request.GET.get('tag')
    if username:
        author = get_object_or_404(User, username=username)
        if tag:
            recipes = author.recipes.filter(tag__name=tag)
        else:
            recipes = author.recipes.all()
    elif request.resolver_match.url_name == 'favorites':
        author = None
        user = request.user
        if tag:
            favors = user.favoriters.filter(recipe__tag__name=tag)
        else:
            favors = user.favoriters.all()
        recipes = Recipe.objects.filter(id__in=favors.values('recipe_id'))
    else:
        author = None
        if tag:
            recipes = Recipe.objects.filter(tag__name=tag)
        else:
            recipes = Recipe.objects.all()
    paginator = Paginator(recipes, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator, tag, author


def index(request):
    page, paginator, tag, author = get_recipes(request)
    return render(
         request,
         'index.html',
         {
             'page': page,
             'paginator': paginator,
             'tag': tag,
         }
    )


def profile(request, username):
    page, paginator, tag, author = get_recipes(request, username)
    return render(
        request,
        'profile.html',
        {
            'page': page,
            'paginator': paginator,
            'author': author,
            'tag': tag,
        }
    )


def recipe_view(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_page.html', {'recipe': recipe})


def get_ingredient(request):
    ingredients = {}
    for key, value in request.POST.items():
        if key.startswith('nameIngredient'):
            number = key.split('_')[1]
            ingredients[value] = request.POST.get(f'valueIngredient_{number}')
    return ingredients


def form_saving(request, form):
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()

    ingredients = get_ingredient(request)
    components = []
    Component.objects.filter(recipe=recipe).delete()
    for title, value in ingredients.items():
        unit = get_object_or_404(Unit, title=title)
        comp = Component(
            recipe=recipe,
            unit=unit,
            value=value
        )
        components.append(comp)
    Component.objects.bulk_create(components)
    form.save_m2m()


@login_required
def new_recipe(request):
    if request.method != "POST":
        form = RecipeForm()
        return render(request, "new_recipe.html", {"form": form})

    form = RecipeForm(request.POST or None, files=request.FILES or None)

    print(request.POST.getlist('tags'))

    if form.is_valid():
        form_saving(request, form)
        return redirect('index')

    return render(request, "new_recipe.html", {"form": form})


@login_required
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if recipe.author != request.user:
        return redirect('recipe', id=id)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )
    if form.is_valid():
        form_saving(request, form)
        return redirect('recipe', id=id)

    return render(
        request,
        "new_recipe.html",
        {"form": form, 'edit': True, 'recipe': recipe}
    )


@login_required
def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.author != request.user:
        return redirect('recipe', id=id)
    recipe.delete()
    return redirect('index')


@login_required
def subscribe(request):
    user = request.user
    all_param = request.GET.get('all')
    all = int(all_param) if all_param else None
    subscriptions = user.subscriber.all()
    paginator = Paginator(subscriptions, 3)

    page_number = request.GET.get('subscriptions')
    subscriptions = paginator.get_page(page_number)
    return render(
        request,
        'subscribes.html',
        {
            'subscriptions': subscriptions,
            'paginator': paginator,
            'all': all,
        }
    )


@login_required
def favorites(request):
    page, paginator, tag, author = get_recipes(request)
    return render(
         request,
         'favorites.html',
         {
             'page': page,
             'paginator': paginator,
             'tag': tag,
         }
    )


@login_required
def purchases(request):
    user = request.user
    purchases = user.buyers.all()
    recipes = Recipe.objects.filter(id__in=purchases.values('recipe_id'))
    return render(
        request,
        'purchases.html',
        {'recipes': recipes}
    )


@login_required
def shoplist_download(request):
    user = request.user
    purchases = user.buyers.all()
    recipes = Recipe.objects.filter(id__in=purchases.values('recipe_id'))
    components = Component.objects.filter(recipe__in=recipes)
    titles = []
    dimensions = []
    values = []
    for comp in components:
        if comp.unit.title in titles:
            index = titles.index(comp.unit.title)
            values[index] += comp.value
        else:
            titles.append(comp.unit.title)
            dimensions.append(comp.unit.dimension)
            values.append(comp.value)

    data = [[titles[i], dimensions[i], values[i]] for i in range(len(titles))]
    return ExcelResponse(data)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
