from rest_framework import serializers
from order.models import Order, Billing
from datetime import datetime


class OrderSerializer(serializers.Serializer):
    
    productType = serializers.IntegerField()
    metadata = serializers.CharField()
    tires = serializers.IntegerField()
    price = serializers.FloatField()
    card_name = serializers.CharField()
    card_number = serializers.CharField()
    cvv = serializers.IntegerField()
    expiry_date = serializers.CharField()

    def save(self, user):
        order = Order()
        order.user = user

        order.product_type = self.validated_data['productType']
        order.metadata = self.validated_data['metadata']
        order.tires = self.validated_data['tires']
        order.completed_date = datetime.utcnow().isoformat()[:-3] + 'Z'
        # price = get_object_or_404(Price, pk = (order.product_type+1))
        # order.price = int(price.price * order.tires * 100)
        order.price = int(self.validated_data['price'] * 100)
        order.status = 0
        order.save()

        billing = Billing()
        billing.order = order
        billing.price = self.validated_data['price']
        billing.card_name = self.validated_data['card_name']
        billing.card_number = self.validated_data['card_number']
        billing.cvv = self.validated_data['cvv']
        billing.expiry_date = self.validated_data['expiry_date']
        billing.save()
        return order
