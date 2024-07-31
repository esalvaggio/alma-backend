import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Card
from essays.models import Essay

@pytest.mark.django_db
class TestCardViews:
    @pytest.fixture(autouse=True)
    def setup_class(self, db, client):
        self.client = client
        self.user = User.objects.create(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.essay = Essay.objects.create(
            user=self.user,
            content="Sample essay content"
        )
        self.card1 = Card.objects.create(
            user=self.user,
            essay=self.essay,
            question="What is the capital of France?",
            answer="Paris",
            next_review_date=timezone.now() - timezone.timedelta(days=1),  # Overdue
            review_count=1
        )
        self.card2 = Card.objects.create(
            user=self.user,
            essay=self.essay,
            question="What is the capital of Germany?",
            answer="Berlin",
            next_review_date=timezone.now() + timezone.timedelta(days=1),  # Due tomorrow
            review_count=1
        )

    def test_review_cards_list_view_default(self):
        response = self.client.get('/api/cards/review')
        assert response.status_code == 200
        assert len(response.json()) == 1  # Should only return overdue cards by default

    def test_review_cards_list_view_include_future(self):
        response = self.client.get('/api/cards/review?include_future=true')
        assert response.status_code == 200
        assert len(response.json()) == 2  # Should return both cards
