from django.urls import path
from .views import JournalEntryList, JournalEntryDetail, JournalEntryCreate, JournalEntryUpdate, JournalEntryDelete

urlpatterns = [
    path('', JournalEntryList.as_view(), name='journal-list'),
    path('<int:pk>/', JournalEntryDetail.as_view(), name='journal-detail'),
    path('', JournalEntryCreate.as_view(), name='journal-create'),
    path('<int:pk>/', JournalEntryUpdate.as_view(), name='journal-update'),
    path('<int:pk>/', JournalEntryDelete.as_view(), name='journal-delete'),
]
