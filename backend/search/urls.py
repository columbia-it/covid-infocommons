from django.urls import path, include
from . import views

urlpatterns = [
    path('grants', views.search_grants, name='search_grants'),
    path('facets', views.get_facet_by_field, name='search_grants'),
    path('publications', views.search_publications, name='search_publications')
]
