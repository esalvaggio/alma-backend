from django.urls import path
from .views import CardListView, ReviewCardsListView, AnswerCardView

urlpatterns = [
    path('', CardListView.as_view(), name='card-list'),
    path('review', ReviewCardsListView.as_view(), name='card-review'),
    path('answer/<int:pk>/', AnswerCardView.as_view(), name='card-answer')
]