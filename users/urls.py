from django.urls import path
from .views import UserAPIView, AddUserAPIView, LoginUserAPIView

urlpatterns = [
    path('<int:id>/', UserAPIView.as_view()),
    path('addUser/', AddUserAPIView.as_view()),
    path('login/', LoginUserAPIView.as_view())
]