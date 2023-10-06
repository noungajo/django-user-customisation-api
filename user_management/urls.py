
from operator import sub
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings
from users.urls import user_urls


schema_view = get_schema_view(
   openapi.Info(
      title="DOTCHE API",
      default_version='v0.0.1',
      description="This api documentation presents the available endpoints of the dotche api and the endpoint requirements.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="fjonathannoutcha@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(user_urls)),
    
    re_path(r'^api/docs/(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
