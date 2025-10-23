from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    # path('activate/', views.ActivateAccountView.as_view(), name='activate'),
]