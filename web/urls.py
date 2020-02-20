"""commgestion URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^stats/$', views.net_stats, name='stats'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^public/$', views.public_info, name='public_info'),
    url(r'^usuario/$', views.usuario, name='usuario'),
    path('', views.home, name='home')
]

# Authentication patterns
urlpatterns += [
    path('login/', auth_views.LoginView.as_view(
        template_name='admin/login.html',
        extra_context={
            'site_header': _('Community Cellular Login')
        }
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

