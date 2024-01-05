"""
URL configuration for libremusique project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PieceViewSet, CollaboratorViewSet, RecitalViewSet, NoteViewSet

router = DefaultRouter()
router.register(r'pieces', PieceViewSet)
router.register(r'collaborators', CollaboratorViewSet)
router.register(r'recitals', RecitalViewSet)
router.register(r'notes', NoteViewSet, basename='note')  # Use basename if queryset is not defined

urlpatterns = [
    path('', include(router.urls)),
    # Add other URLs here as needed
]

