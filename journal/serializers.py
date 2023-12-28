from rest_framework import serializers
from .models import JournalEntry, TextElement

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id','title','created_at']

class TextElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextElement
        fields = ['id','journal_entry', 'content', 'is_ai', 'created_at']