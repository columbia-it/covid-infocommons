from django.urls import path
from . import views
from search.views import index, pi_detail

urlpatterns = [
    path('', index),
    path('grants', views.search_grants, name='search_grants'),
    path('facets', views.get_facet_by_field, name='search_grants'),
    path('facets/people', views.get_people_facet_by_field, name='people_facet'),
    path('facets/publications/authors', views.get_pub_author_facet, name='pub_author_facet'),
    path('facets/datasets/authors', views.get_dataset_author_facet, name='dataset_author_facet'),
    path('publications', views.search_publications, name='search_publications'),
    path('people', views.search_people, name='search_people'),
    path('people/pi/<int:pi_id>', pi_detail),
    path('datasets', views.search_datasets, name='search_datasets'),
    path('assets', views.search_assets, name='search_assets')
]
