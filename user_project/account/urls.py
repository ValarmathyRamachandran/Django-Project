from django.urls import path
from .views import LoginApiView, LogoutApiView, RegistrationApiView, ActivateApiView, ResetPasswordApiView

urlpatterns = [
    path('register/', RegistrationApiView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view()),
    path('activate/', ActivateApiView.as_view(), name='activate'),
    path('resetpassword/', ResetPasswordApiView.as_view())
]

