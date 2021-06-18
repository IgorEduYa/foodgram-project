import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

from recipes.models import Recipe, User, Unit
from .models import Purchases, Favorites, Subscription


@csrf_protect
@require_http_methods(['POST'])
def add_to_shoplist(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['id']
    recipe = Recipe.objects.get(id=id)
    purchase = Purchases.objects.create(
        user=request.user,
        recipe=recipe
    )
    purchase.save()
    return JsonResponse({"success": True})


@csrf_protect
@require_http_methods(['DELETE'])
def remove_from_shoplist(request, id):
    recipe = Recipe.objects.get(id=id)
    purchase = get_object_or_404(
        Purchases,
        recipe=recipe,
        user=request.user
    )
    purchase.delete()
    return JsonResponse({"success": True})


@csrf_protect
@require_http_methods(['POST'])
def add_to_favorite(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['id']
    recipe = Recipe.objects.get(id=id)
    favorite = Favorites.objects.create(
        user=request.user,
        recipe=recipe
    )
    favorite.save()
    return JsonResponse({"success": True})


@csrf_protect
@require_http_methods(['DELETE'])
def remove_from_favorite(request, id):
    recipe = Recipe.objects.get(id=id)
    favorite = get_object_or_404(
        Favorites,
        recipe=recipe,
        user=request.user
    )
    favorite.delete()
    return JsonResponse({"success": True})


@csrf_protect
@require_http_methods(['POST'])
def subscribe(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['id']
    author = get_object_or_404(User, id=id)
    if request.user.username != author.username:
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            author=author
        )
        subscription.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@csrf_protect
@require_http_methods(['DELETE'])
def unsubscribe(request, id):
    author = get_object_or_404(User, id=id)
    if Subscription.objects.filter(
            author=author).filter(user=request.user).exists():
        subscription = get_object_or_404(
            Subscription,
            author=author,
            user=request.user
        )
        subscription.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@csrf_protect
@require_http_methods(['GET'])
def get_ingredients(request):
    query_string = request.GET.get('query')
    result = list(Unit.objects.filter(
        title__startswith=str(query_string)).values('title', 'dimension'))
    return JsonResponse(result, safe=False)
