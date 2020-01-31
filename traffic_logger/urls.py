"""traffic_logger URL Configuration
"""
from django.urls import re_path
from traffic_logger import views

urlpatterns = [
    re_path('^user/?$', views.log_user_throughput, name='log-user-throughput'),
    re_path('^host/?$', views.log_host_throughput, name='log-host-throughput'),
]
