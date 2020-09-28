from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'list', views.OrderViewSet.as_view({'get': 'list'})),
    url(r'create', views.OrderViewSet.as_view({'post': 'create'})),
    url(r'commit', views.OrderCommit.as_view()),
]
