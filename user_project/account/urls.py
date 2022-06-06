from django.urls import path
from .views import RegistrationAPIView, LoginApiView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
]

