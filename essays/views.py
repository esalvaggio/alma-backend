from rest_framework import generics
from .models import Essay
from .serializers import EssaySerializer
from rest_framework.permissions import IsAuthenticated
from cards.services import main as generate_and_create_cards

class BaseEssayViewSet(generics.GenericAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer
    permission_classes = [IsAuthenticated]

class EssayListCreateAPIView(BaseEssayViewSet, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        essay = serializer.save(user=self.request.user)
        generate_and_create_cards(essay)


class EssayDetailAPIView(BaseEssayViewSet, generics.RetrieveUpdateDestroyAPIView):
    pass

class EssayListDeleteAPIView(BaseEssayViewSet, generics.DestroyAPIView):
    pass
