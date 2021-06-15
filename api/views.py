from .viewsets import CreateDestroyViewSet
from .models import Purchases, Favorites, Subscription
from .serializers import (PurchaseSerializer,
                          FavoriteSerializer,
                          SubscriptionSerializer)


class PurchaseViewSet(CreateDestroyViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchaseSerializer


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoriteSerializer


class SubscriptionViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
