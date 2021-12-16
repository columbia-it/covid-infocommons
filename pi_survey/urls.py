from django.urls import path, include, re_path
from rest_framework import routers, permissions
from .views import index

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', index),
]
