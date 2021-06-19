import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from recipes.models import Recipe, Unit, User
from rest_framework import status

from .models import Favorites, Purchases, Subscription


@csrf_protect
@require_http_methods(['POST'])
def add_to_shoplist(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body.get('id')
    recipe = get_object_or_404(Recipe, id=id)
    purchase = Purchases.objects.create(
        user=request.user,
        recipe=recipe
    )
    purchase.save()
    return JsonResponse({"success": True}, status=status.HTTP_201_CREATED)


@csrf_protect
@require_http_methods(['DELETE'])
def remove_from_shoplist(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    purchase = get_object_or_404(
        Purchases,
        recipe=recipe,
        user=request.user
    )
    purchase.delete()
    return JsonResponse({"success": True}, status=status.HTTP_200_OK)


@csrf_protect
@require_http_methods(['POST'])
def add_to_favorite(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body.get('id')
    recipe = get_object_or_404(Recipe, id=id)
    favorite = Favorites.objects.create(
        user=request.user,
        recipe=recipe
    )
    favorite.save()
    return JsonResponse({"success": True}, status=status.HTTP_201_CREATED)


@csrf_protect
@require_http_methods(['DELETE'])
def remove_from_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    favorite = get_object_or_404(
        Favorites,
        recipe=recipe,
        user=request.user
    )
    favorite.delete()
    return JsonResponse({"success": True}, status=status.HTTP_200_OK)


@csrf_protect
@require_http_methods(['POST'])
def subscribe(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body.get('id')
    author = get_object_or_404(User, id=id)
    if request.user.username != author.username:
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            author=author
        )
        subscription.save()
        return JsonResponse({"success": True}, status=status.HTTP_201_CREATED)
    return JsonResponse({"success": False}, status=status.HTTP_403_FORBIDDEN)


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
        return JsonResponse({"success": True}, status=status.HTTP_200_OK)
    return JsonResponse({"success": False}, status=status.HTTP_403_FORBIDDEN)


@csrf_protect
@require_http_methods(['GET'])
def get_ingredients(request):
    query_string = request.GET.get('query')
    result = list(Unit.objects.filter(
        title__istartswith=str(query_string)).values('title', 'dimension'))
    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
