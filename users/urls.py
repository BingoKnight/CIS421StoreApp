from django.urls import path
from .views import UserAPIView, AddUserAPIView

urlpatterns = [
    path('allUsers/', UserAPIView.as_view()),
    path('addUser/', AddUserAPIView.as_view()),
]