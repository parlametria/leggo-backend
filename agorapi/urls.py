from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title='API Ágora Digital',
      default_version='v1',
      description='Acesso aos dados de proposições do Congresso.',
      # terms_of_service='https://www.google.com/policies/terms/',
      # contact=openapi.Contact(email='contact@snippets.local'),
      license=openapi.License(name='AGPL License'),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    url(r'^', include('api.urls'))
]
