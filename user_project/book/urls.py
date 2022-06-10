from django.urls import path
from .views import AddBookAPI

urlpatterns = [
    path('book/', AddBookAPI.as_view(), name='book operations'),

]
