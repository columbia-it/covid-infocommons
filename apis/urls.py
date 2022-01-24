from rest_framework import routers, permissions
from .views import PersonViewSet, OrganizationViewSet, GrantViewSet, GrantRelationshipView, PublicationViewSet, PersonRelationshipView, DatasetViewSet, DatasetRelationshipView, AssetViewSet
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from apis.schemas import SchemaGenerator
from django.views.generic.base import RedirectView, TemplateView
from apis import __title__


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'people', PersonViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'grants', GrantViewSet)
router.register(r'publications', PublicationViewSet)
router.register(r'datasets', DatasetViewSet)
router.register(r'assets', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('organizations/<pk>', OrganizationViewSet.as_view({'put':'update'}), name='organization-detail'),
    path('openapi', get_schema_view(generator_class=SchemaGenerator, public=True),
         name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema', 'title': __title__}), name='swagger-ui'),
    # person relationships:
    path('people/<pk>/relationships/<related_field>',
        PersonRelationshipView.as_view(),
        name='person-relationships'),
    path('people/<pk>/<related_field>',
        PersonViewSet.as_view({'get': 'retrieve_related'}),
        name='person-related'),
    # publication relationships:
    path('publications/<pk>/relationships/<related_field>',
        PersonRelationshipView.as_view(),
        name='publication-relationships'),
    path('publications/<pk>/<related_field>',
        PublicationViewSet.as_view({'get': 'retrieve_related'}),
        name='publication-related'),
    # grant relationships:
    path('grants/<pk>/relationships/<related_field>',
        GrantRelationshipView.as_view(),
        name='grant-relationships'),
    path('grants/<pk>/<related_field>',
        GrantViewSet.as_view({'get': 'retrieve_related'}),
        name='grant-related'),
    # dataset relationships:
    path('datasets/<pk>/relationships/<related_field>',
        DatasetRelationshipView.as_view(),
        name='dataset-relationships'),
    path('datasets/<pk>/<related_field>',
        DatasetViewSet.as_view({'get': 'retrieve_related'}),
        name='dataset-related'),
]