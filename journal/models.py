from django.db import models
from django.conf import settings

class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.created_at}" if self.title else f"Entry Created at {self.created_at}"

class TextElement(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, related_name='elements', on_delete=models.CASCADE)
    content = models.TextField()  # Consider encryption if privacy is a concern
    is_ai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Element from {self.journal_entry.created_at} - {'AI' if self.is_ai else 'User'} Generated"
    