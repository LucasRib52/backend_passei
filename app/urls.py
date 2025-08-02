"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuração da documentação da API
schema_view = get_schema_view(
    openapi.Info(
        title="EduConcursos API",
        default_version='v1',
        description="API para a plataforma EduConcursos - Sistema de Cursos Online",
        terms_of_service="https://www.educoncursos.com/terms/",
        contact=openapi.Contact(email="contato@educoncursos.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/v1/courses/', include('courses.urls')),
    path('api/v1/professors/', include('professors.urls')),
    path('api/v1/testimonials/', include('testimonials.urls')),
    path('api/v1/news/', include('news.urls')),
    path('api/v1/sales/', include('sales.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/categories/', include('courses.category_urls')),
    
    # Documentação da API
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Configuração para arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
