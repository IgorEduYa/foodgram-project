from django.urls import path

from . import views


urlpatterns = [
    path('<slug:tag>/', views.index, name='tag_index'),
    path('', views.index, name='index'),
]
