from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import generics, status
from .models import Card
from .serializers import CardSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class CardListView(generics.ListAPIView):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Card.objects.filter(user=user)
        essay_id = self.request.query_params.get('essay_id', None)
        if essay_id is not None:
            queryset = queryset.filter(essay_id=essay_id)
        return queryset
    
class ReviewCardsListView(generics.ListAPIView):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view returns a list of all the cards that are due for review for the requesting user,
        optionally including those with past due dates.
        """
        today = timezone.now().date()
        include_future = self.request.query_params.get('include_future', 'false').lower() == 'true'

        queryset = Card.objects.filter(user=self.request.user)
        if not include_future:
            queryset = queryset.filter(user=self.request.user, next_review_date__date__lte=today)
        return queryset.order_by('next_review_date')
class AnswerCardView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Handle answering the card and adjusting the next review date.
        Accepts 'correct' (true/false) as a POST parameter.
        """
        
        card = get_object_or_404(Card, pk=pk, user=request.user)

        correct = request.data.get('correct')
        if isinstance(correct, bool) is False:
            raise ValidationError("Field 'correct' must be a boolean.")
        if correct is None:
            raise ValidationError("Field 'correct' is required and should be either true or false.")
        card.update_review(correct)
        
        return Response({
            'status': 'success',
            'next_review_date': card.next_review_date,
            'review_interval': card.review_interval,
            'review_count': card.review_count
        }, status=status.HTTP_200_OK)
