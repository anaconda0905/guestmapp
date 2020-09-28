"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from users import views
from order import views as order_views
from scan import views as scan_views
from backend import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # admin part
    path('admin/', admin.site.urls),

    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    # administration
    path('administration/', include('administration.urls')),
    path('dashboard/', include('dashboard.urls')),

    # api part
    path('api/auth/', include('users.urls')),
    path('api/order/', include('order.urls')),
    path('api/scan/', include('scan.urls')),
    path('api/price/', include('price.urls')),

    path('api/mobilehome2dtype/', include('hometype.urls')),

    # for ajax handler
    path(r'ajax_login/', views.ajax_login, name = "ajax_login"),
    path(r'ajax_register/', views.ajax_register, name = "ajax_register"),
    path(r'ajax_logout/', views.ajax_logout, name="ajax_logout"),

    # for stripe integrtion
    path(r'payout/', order_views.payout, name="payout"),

    # upload scan
    path(r'progress_bar_upload/', scan_views.ProgressBarUpload, name='progress_bar_upload'),
    path(r'uploadscan/', scan_views.uploadscan, name='uploadscan'),
    path(r'uploadtitle/', scan_views.uploadtitle, name='uploadtitle'),
    # upload detail
    path(r'getDatailbyId/', scan_views.getDatailbyId, name='getDatailbyId'),
    path(r'uploadscandetail/', scan_views.uploadscandetail, name='uploadscandetail'),
    path(r'uploadDetialTitle/', scan_views.uploadDetialTitle, name='uploadDetialTitle'),
    path(r'orderReady/', scan_views.orderReady, name='orderReady'),
    path(r'orderConfirmed/', scan_views.orderConfirmed, name='orderConfirmed'),

    # order ready state
    path(r'removeDetail/', scan_views.removeDetail, name='removeDetail'),

    # for web template
    path(r'', views.home, name="home"),
    path(r'planprices/', views.planprices, name = "planprices"),
    path(r'ownguestmapp/', views.ownguestmapp, name="ownguestmapp"),
    path(r'guestmapp/', views.guestmapp, name = "guestmapp"),
    path(r'newpassword/', views.newpassword),

    # media part and administration static part
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    url(r'^administration/static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, }),
    url(r'^administration/all_orders/static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, }),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
