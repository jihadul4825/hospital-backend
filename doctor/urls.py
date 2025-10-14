from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'list', views.DoctorViewSet)
router.register(r'designation', views.DesignationViewSet)
router.register(r'specialization', views.SpecializationViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'available_time', views.AvailableTimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]