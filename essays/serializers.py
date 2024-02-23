from rest_framework import serializers
from .models import Essay

class EssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['id','user','title','content','author','created_at','source_url', 'summary','publication_date']
        read_only_fields = ('user',)

class EssayMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['id', 'title', 'author']