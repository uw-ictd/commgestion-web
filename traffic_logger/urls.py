"""traffic_logger URL Configuration
"""
from django.urls import re_path
from traffic_logger import views

urlpatterns = [
    re_path("^user/?$", views.log_subscriber_usage, name="log-user-throughput"),
    re_path("^host/?$", views.log_host_usage, name="log-host-throughput"),
    re_path("^ran/?$", views.log_ran_usage, name="log-ran-usage"),
    re_path("^backhaul/?$", views.log_backhaul_usage, name="log-backhaul-usage"),
]
