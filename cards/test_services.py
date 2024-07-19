import pytest
from django.utils import timezone
from unittest.mock import patch
from .services import generate_card_data, create_cards
from .models import Card
from essays.models import Essay

# @pytest.mark.django_db
# def test_valid_json_response():
#     essay = Essay(content="Example essay content")
#     valid_json = {
#         'choices': [{
#             'message': {
#                 'content': '{"questions": [{"question": "What is 2+2?", "answer": "4", "percent_through": 50}]}'
#             }
#         }]
#     }
#     with patch('requests.post') as mock_post:
#         mock_post.return_value.status_code = 200
#         mock_post.return_value.json.return_value = valid_json
#         response = generate_card_data(essay)
#         assert response is not None
#         assert 'choices' in response
#         is_created = create_cards(essay, response)
#         assert is_created is True
#         assert Card.objects.count() == 1

# @pytest.mark.django_db
# def test_invalid_json_response():
#     essay = Essay(content="Another example essay content")
#     invalid_json = {
#         'choices': [{
#             'message': {
#                 'content': 'This is not JSON'
#             }
#         }]
#     }
#     with patch('requests.post') as mock_post:
#         mock_post.return_value.status_code = 200
#         mock_post.return_value.json.return_value = invalid_json
#         response = generate_card_data(essay)
#         assert response is not None
#         with patch('logging.Logger.error') as mock_log:
#             is_created = create_cards(essay, response)
#             assert is_created is False
#             mock_log.assert_called()

# def test_handle_errors():
#     with patch('requests.post') as mock_post:
#         mock_post.return_value.status_code = 500
#         mock_post.return_value.text = 'Internal Server Error'
#         response = generate_card_data(Essay(content=""))
#         assert response is None
#         with patch('logging.Logger.error') as mock_log:
#             create_cards(Essay(content=""), None)
#             mock_log.assert_called()

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

def test_handle_errors():
    with patch('logging.Logger.error') as mock_log:
        response = generate_card_data(Essay(content=""))
        assert response is None
        mock_log.assert_called_once()
