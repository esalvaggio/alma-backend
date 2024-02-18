from django.db import models
from django.conf import settings

class Essay(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    source_url = models.URLField(max_length=2000, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.created_at}" if self.title else f"Essay Created at {self.created_at}"