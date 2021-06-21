import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from recipes.models import Recipe, Unit, User
from rest_framework import status

from .models import Favorites, Purchases, Subscription


def create_object(request, obj_model, sub_model):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body.get('id')
    sub_obj = get_object_or_404(sub_model, id=id)
    if obj_model == Subscription:
        if request.user.username != sub_obj.username:
            subscription, created = obj_model.objects.get_or_create(
                user=request.user,
                author=sub_obj
            )
            subscription.save()
            return JsonResponse({"success": True},
                                status=status.HTTP_201_CREATED)
        return JsonResponse({"success": False},
                            status=status.HTTP_403_FORBIDDEN)
    obj = obj_model.objects.create(
        user=request.user,
        recipe=sub_obj
    )
    obj.save()
    return JsonResponse({"success": True}, status=status.HTTP_201_CREATED)


def delete_object(request, obj_model, id, sub_model):
    sub_obj = get_object_or_404(sub_model, id=id)
    if obj_model == Subscription:
        if Subscription.objects.filter(
                author=sub_obj).filter(user=request.user).exists():
            subscription = get_object_or_404(
                Subscription,
                author=sub_obj,
                user=request.user
            )
            subscription.delete()
            return JsonResponse({"success": True}, status=status.HTTP_200_OK)
        return JsonResponse({"success": False},
                            status=status.HTTP_403_FORBIDDEN)
    obj = get_object_or_404(
        obj_model,
        recipe=sub_obj,
        user=request.user
    )
    obj.delete()
    return JsonResponse({"success": True}, status=status.HTTP_200_OK)


@csrf_protect
@require_http_methods(['POST'])
def add_to_shoplist(request):
    return create_object(request, Purchases, Recipe)


@csrf_protect
@require_http_methods(['DELETE'])
def remove_from_shoplist(request, id):
    return delete_object(request, Purchases, id, Recipe)


@csrf_protect
@require_http_methods(['POST'])
def add_to_favorite(request):
    return create_object(request, Favorites, Recipe)


@csrf_protect
@require_http_methods(['DELETE'])
def remove_from_favorite(request, id):
    return delete_object(request, Favorites, id, Recipe)


@csrf_protect
@require_http_methods(['POST'])
def subscribe(request):
    return create_object(request, Subscription, User)


@csrf_protect
@require_http_methods(['DELETE'])
def unsubscribe(request, id):
    return delete_object(request, Subscription, id, User)


@csrf_protect
@require_http_methods(['GET'])
def get_ingredients(request):
    query_string = request.GET.get('query')
    result = list(Unit.objects.filter(
        title__istartswith=str(query_string)).values('title', 'dimension'))
    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
