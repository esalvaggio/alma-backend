from django.db import models

class Card(models.Model):
    essay = models.ForeignKey('essays.Essay', related_name="cards", on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    percent_through = models.IntegerField()
    next_review_date = models.DateTimeField()
    review_interval = models.IntegerField(default=1)
    review_count = models.IntegerField(default=0)

def __str__(self):
        return self.question