from rest_framework import generics
from .models import JournalEntry
from .serializers import JournalEntrySerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class JournalEntryList(generics.ListAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class JournalEntryDetail(generics.RetrieveAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

class JournalEntryCreate(generics.CreateAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JournalEntryUpdate(generics.UpdateAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

class JournalEntryDelete(generics.DestroyAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]
