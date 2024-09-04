from django.db import models
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

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
        return self.questions
    
    def update_review(self, correct):
        """updates the review date and interval based on whether the answer was correct"""
        if correct:
            self.review_interval = int(self.review_interval * 1.5) # maybe change this
        else:
            self.review_interval = 1

        self.next_review_date = timezone.now() + timezone.timedelta(days=self.review_interval)
        self.review_count += 1
        self.save()

        logger.info(f"Card {self.pk} updated. Correct: {correct}. Next review: {self.next_review_date}")
