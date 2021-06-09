from django.urls import path

from . import views


urlpatterns = [
    path('recipe/<int:id>/', views.recipe_view, name='recipe'),
    path('profile/<str:username>/<slug:tag>/', views.profile, name='tag_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('<slug:tag>/', views.index, name='tag_index'),
    path('', views.index, name='index'),
]
