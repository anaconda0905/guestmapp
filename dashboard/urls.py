from django.contrib.auth.views import LogoutView
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index, name='admin_dashboard'),
    url(r'^login/$', views.login_view, name="sign"),
    url(r'^all_orders/$', views.all_orders, name="all_orders"),
    url(r'^test/$', views.test, name="test"),
    url(r'^register/$', views.register_user, name="register"),
    url(r"^logout/$", LogoutView.as_view(), name="logout")
]