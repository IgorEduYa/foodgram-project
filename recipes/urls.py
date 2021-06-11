from django.urls import path

from . import views


urlpatterns = [
    path('purchases/', views.purchases, name='purchases'),
    path('favorites/', views.favorites, name='favorites'),
    path('subscribes/', views.subscribe, name='subscribe'),
    path('recipe/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:id>/', views.recipe_view, name='recipe'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('', views.index, name='index'),
]
