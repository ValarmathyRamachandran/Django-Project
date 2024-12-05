from django.urls import path

from .views import OrderCheckoutApiView

urlpatterns = [
    path('ordercheckout/', OrderCheckoutApiView.as_view()),

]