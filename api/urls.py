from django.urls import path

from . import views


urlpatterns = [
    path(
        'v1/purchases/',
        views.add_to_shoplist,
        name='add_to_shop'
    ),
    path(
        'v1/purchases/<int:id>/',
        views.remove_from_shoplist,
        name='remove_from_shoplist'
    ),
    path(
        'v1/favorites/',
        views.add_to_favorite,
        name='add_to_favorite'
    ),
    path(
        'v1/favorites/<int:id>/',
        views.remove_from_favorite,
        name='remove_from_favorite'
    ),
    path(
        'v1/subscriptions/',
        views.subscribe,
        name='subscribe'
    ),
    path(
        'v1/subscriptions/<int:id>/',
        views.unsubscribe,
        name='unsubscribe'
    ),
    path(
        'v1/ingredients/',
        views.get_ingredients,
        name='get_ingredients'
    )
]
