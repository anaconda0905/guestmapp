from django.http import JsonResponse
from price.models import Price
from price.serializers import PriceSerializer
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class PriceViewSet(ModelViewSet):
    http_method_names = ['post', 'get']
    serializer_class = PriceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Price.objects.all()

    def list(self, request, *args, **kwargs):
        prices = self.get_queryset()

        return JsonResponse({
            "success": True,
            "message": "success to get price list",
            "errCode": -1,
            "data": [price.to_dict() for price in prices]
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        price = serializer.save()
        return JsonResponse({
            "success": True,
            "message": "success to create new price",
            "errCode": -1,
            "data": price.to_dict()
        }, status=status.HTTP_200_OK)
