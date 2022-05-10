from django.urls import path, include
from . import views

urlpatterns = [
    path('grants', views.search_grants, name='search_grants')]