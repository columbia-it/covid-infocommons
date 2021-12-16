from rest_framework import routers, permissions
from .views import PersonViewSet, OrganizationViewSet, GrantViewSet
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'people', PersonViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'grants', GrantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

schema_view = get_schema_view(openapi.Info(
    title='CIC API',
    default_version='0.1',
    description='API for Covid Information Commons',),
    public=True, permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    )
]