from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'get', views.ScanTableApiViewSet.as_view({'get': 'list'})),
    url(r'create', views.ScanTableApiViewSet.as_view({'post': 'create'})),
    url(r'details/list', views.ScanDetailsTableApiViewSet.as_view({'get': 'list'})),
    url(r'details/add', views.ScanDetailsTableApiViewSet.as_view({'post': 'create'})),
    url(r'details/delete', views.ScanDetailsTableApiViewSet.as_view({'post': 'remove'})),
]
