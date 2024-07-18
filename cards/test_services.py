import pytest
from django.utils import timezone
from unittest.mock import patch
from .services import generate_card_data, create_cards
from .models import Card
from essays.models import Essay

# Todo: make these tests test my code properly 
@pytest.mark.django_db
def test_generate_card_data():
    essay = Essay(content="Your essay content here")
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "questions": "<expected JSON structure here>"
        }
        response = generate_card_data(essay)
        assert response is not None
        assert "questions" in response

@pytest.mark.django_db
def test_create_cards():
    essay = Essay(content="Test essay content")
    cards_data = {
        "questions": [
            {
                "question": "What is the meaning of life?",
                "answer": "42",
                "percent_through": 50
            }
        ]
    }
    success = create_cards(essay, cards_data)
    assert success is False
    assert Card.objects.count() == 1
    card = Card.objects.first()
    assert card.question == "What is the meaning of life?"
    assert card.answer == "42"
    assert card.percent_through == 50
    assert card.review_count == 0

def test_handle_errors():
    with patch('logging.Logger.error') as mock_log:
        response = generate_card_data(Essay(content=""))
        assert response is None
        mock_log.assert_called_once()
