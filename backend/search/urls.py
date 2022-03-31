from django.urls import path, include
from . import views

urlpatterns = [
    path('grants', views.GrantSearch.as_view(), name='search_grants')]