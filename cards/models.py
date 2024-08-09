from django.db import models
from django.conf import settings

class Card(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    essay = models.ForeignKey('essays.Essay', related_name="cards", on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    percent_through = models.IntegerField()
    next_review_date = models.DateTimeField()
    review_interval = models.IntegerField(default=1)
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.question