"""Mri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from MriApi.views import (ResearchAPIView, ProfileAPIView, StartAPIView, CreateReportAPIView, CreateArchiveAPIView, RegistrationAPIView)
from Mri import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/research/', ResearchAPIView.as_view(), name='research'),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('accounts/profile/', ProfileAPIView.as_view()),
    path('api/v1/start/', StartAPIView.as_view(), name='start'),
    path('api/v1/report/', CreateReportAPIView.as_view(), name='report'),
    path('api/v1/archive/', CreateArchiveAPIView.as_view(), name='archive'),
    path('api/v1/registration/', RegistrationAPIView.as_view(), name='registration')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
