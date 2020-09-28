from django.http import JsonResponse, HttpResponse
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from hometype.models import HomeType


class HomeTypeViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        hometypes = HomeType.objects.all()
        return JsonResponse({
            "success": True,
            "message": "success to get home type list",
            "errCode": -1,
            "data": [hometype.to_dict() for hometype in hometypes]
        }, status=status.HTTP_200_OK)
