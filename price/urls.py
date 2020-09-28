from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'list', views.PriceViewSet.as_view({'get': 'list'})),
    url(r'create', views.PriceViewSet.as_view({'post': 'create'})),
]
