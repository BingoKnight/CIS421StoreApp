from django.urls import path
from .views import ProductAPIView, ProductSearchAPIView

urlpatterns = [
    path('', ProductAPIView.as_view()),
    path('search/', ProductSearchAPIView.as_view()),
]
