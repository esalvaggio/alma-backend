from django.urls import path
from .views import EssayListCreateAPIView, EssayDetailAPIView, EssayMinimalListView, EssayListDeleteAPIView

urlpatterns = [
    path('', EssayListCreateAPIView.as_view(), name='essay-list-create'),
    path('<int:pk>/', EssayDetailAPIView.as_view(), name='essay-detail'),
    path('minimal/', EssayMinimalListView.as_view(), name='essay-minimal-list'),
]