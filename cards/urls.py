from django.urls import path
from .views import CardListView, ReviewCardsListView

urlpatterns = [
    path('', CardListView.as_view(), name='card-list'),
    path('review', ReviewCardsListView.as_view(), name='card-review')
]