from django.urls import path
from .views import EssayListCreateAPIView, EssayDetailAPIView

urlpatterns = [
    path('', EssayListCreateAPIView.as_view(), name='essay-list-create'),
    path('<int:pk>/', EssayDetailAPIView.as_view(), name='essay-detail'),
]