from rest_framework import serializers

from .models import Purchases, Subscription, Favorites


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'
