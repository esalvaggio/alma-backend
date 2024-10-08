from rest_framework import generics, serializers
from .models import Essay
from django.db import transaction
from .serializers import EssayMinimalSerializer, EssaySerializer
from rest_framework.permissions import IsAuthenticated
from cards.services import main as generate_and_create_cards
import logging
logger = logging.getLogger(__name__)
class BaseEssayViewSet(generics.GenericAPIView):
    serializer_class = EssaySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
         return Essay.objects.filter(user = self.request.user)

class EssayListCreateAPIView(BaseEssayViewSet, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        with transaction.atomic():
            essay = serializer.save(user=self.request.user)
            success = generate_and_create_cards(essay)
            if not success:
                raise serializers.ValidationError("Failed to create cards for the essay.")

class EssayDetailAPIView(BaseEssayViewSet, generics.RetrieveUpdateDestroyAPIView):
    pass

class EssayMinimalListView(BaseEssayViewSet, generics.ListAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayMinimalSerializer
    permission_classes = [IsAuthenticated]