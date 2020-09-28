from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login', views.Login.as_view(), name='login'),
    url(r'signup', views.SignUp.as_view(), name='signup'),
    url(r'update', views.Update.as_view(), name='update'),
]
