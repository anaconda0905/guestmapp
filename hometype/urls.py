from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'list', views.HomeTypeViewSet.as_view({'get': 'list'})),
]
