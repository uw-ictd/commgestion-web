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

from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^api/v1/utilization/?$', views.api.public_utilization, name="public_utilization_api"),
    url(r'^network/stats/?$', views.network_stats, name='network_stats'),
    url(r'^profiles/?$', views.profiles, name='profiles'),
    url(r'^network/users/?$', views.network_users, name='network_users'),
    url(r'^profiles/addform/?$', views.add_form, name='add_form'),
    url(r'^profiles/editform/?$', views.edit_form, name='edit_form'),
    url(r'^profiles/deleteform/?$', views.delete_form, name='delete_form'),
    path('', views.public_info, name='home')
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

