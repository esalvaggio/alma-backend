from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'essay', 'question', 'answer', 'next_review_date', 'review_interval', 'review_count']
