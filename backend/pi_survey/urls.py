from django.urls import path, include, re_path
from rest_framework import routers, permissions
from .views import grant_create_view

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('create/', grant_create_view),
]
