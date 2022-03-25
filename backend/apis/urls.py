from rest_framework import routers
from .views import PersonViewSet, OrganizationViewSet, GrantViewSet, PublicationViewSet, DatasetViewSet, AssetViewSet
from django.urls import path, include, re_path
from rest_framework.schemas import get_schema_view
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
    # path('organizations/<pk>', OrganizationViewSet.as_view({'put':'update'}), name='organization-detail'),
    path('openapi', get_schema_view(generator_class=SchemaGenerator, public=True),
         name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema', 'title': __title__}), name='swagger-ui'),
]