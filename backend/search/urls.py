from django.urls import path
from . import views
from search.views import index

urlpatterns = [
    path('', index),
    path('grants', views.search_grants, name='search_grants'),
    path('facets', views.get_facet_by_field, name='search_grants'),
    path('publications', views.search_publications, name='search_publications'),
    path('people', views.search_people, name='search_people'),
    path('datasets', views.search_datasets, name='search_datasets'),
    path('assets', views.search_assets, name='search_assets')
]
