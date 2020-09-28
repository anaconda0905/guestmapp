from rest_framework import serializers
from .models import Price


class PriceSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.FloatField()
    unit = serializers.CharField()

    def save(self):
        price = Price()
        price.title = self.validated_data['title']
        price.price = self.validated_data['price']
        price.old_price = price.price
        price.unit = self.validated_data['unit']
        price.save()

        return price
