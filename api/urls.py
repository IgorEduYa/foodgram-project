from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PurchaseViewSet, FavoriteViewSet, SubscriptionViewSet


router = DefaultRouter()
router.register(
    r'purchases/(?P<id>\d+)/',
    PurchaseViewSet,
    'purchase'
)
router.register(
    r'subscriptions/(?P<id>\d+)/',
    SubscriptionViewSet,
    'subscription'
)
router.register(
    r'favorites/(?P<id>\d+)/',
    FavoriteViewSet,
    'favorites'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
