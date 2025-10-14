from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ContactUsViewSet


router = DefaultRouter()

router.register(r'', ContactUsViewSet, basename='contactus')
urlpatterns = [
    path('', include(router.urls)),
]

