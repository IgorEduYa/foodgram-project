from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm
from .models import Recipe, User


def index(request):
    tag = request.GET.get('tag')
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
         {'page': page, 'paginator': paginator, 'tag': tag}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    tag = request.GET.get('tag')
    if tag:
        recipes = author.recipes.filter(tag__name=tag)
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
            'tag': tag,
        }
    )


def recipe_view(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_page.html', {'recipe': recipe})


@login_required
def new_recipe(request):
    if request.method != "POST":
        form = RecipeForm()
        return render(request, "new_recipe.html", {"form": form})

    form = RecipeForm(request.POST)

    if form.is_valid():
        to_save = form.save(commit=False)
        to_save.author = request.user
        to_save.save()
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
        to_save = form.save(commit=False)
        to_save.author = request.user
        to_save.save()
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
    if all_param:
        all = int(all_param)
    else:
        all = None
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
    user = request.user
    tag = request.GET.get('tag')
    if tag:
        favors = user.favoriters.filter(recipe__tag__name=tag)
    else:
        favors = user.favoriters.all()

    recipes = []

    for favor in favors:
        recipes.append(favor.recipe)

    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
         request,
         'favorites.html',
         {'page': page, 'paginator': paginator, 'tag': tag}
    )


@login_required
def purchases(request):
    user = request.user
    purchases = user.buyers.all()
    recipes = []
    for purchase in purchases:
        recipes.append(purchase.recipe)
    return render(
        request,
        'purchases.html',
        {'recipes': recipes}
    )
