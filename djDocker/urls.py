"""djDocker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from myapp.views import ArticleAPIView, ArticleSearchAPIView, DetailArticleApiView

schema_view = get_schema_view(
    openapi.Info(
        title="Ulipidia API",
        default_version='v01',
        description="Final Assignment Cloud Integration - Msc. Applied Software Development - CCT",
        github="https://github.com/ulirotela/",
        contact=openapi.Contact(email="ulirotela@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()

router.register('index', ArticleAPIView, basename='index')
router.register('search', ArticleSearchAPIView, basename='search')
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('rest_framework.urls')),
                  path('document/<slug>', DetailArticleApiView.as_view()),
                  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema')
              ] + router.urls
