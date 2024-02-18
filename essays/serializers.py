from rest_framework import serializers
from .models import Essay

class EssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['id','user','title','author','created_at','source_url', 'summary','publication_date']
        read_only_fields = ('user',)