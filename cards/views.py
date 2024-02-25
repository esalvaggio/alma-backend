from rest_framework import generics
from .models import Card
from .serializers import CardSerializer

class CardListView(generics.ListAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.all()
        essay_id = self.request.query_params.get('essay_id', None)
        if essay_id is not None:
            queryset = queryset.filter(essay_id=essay_id)
        return queryset