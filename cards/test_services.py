import pytest
from django.utils import timezone
from unittest.mock import patch
from user.models import User
from .services import generate_card_data, create_cards
from .models import Card
from essays.models import Essay

@pytest.mark.django_db
def test_valid_json_response():
    user = User.objects.create_user(username='testuser', password='password')
    essay = Essay(
        user=user,
        content="Example essay content"
    )
    essay.save()
    valid_json = {
        'choices': [{
            'index': 0,
            'message': {
                'role': 'assistant',
                'content': "{\n  \"questions\": [\n    {\n      \"question\": \"What is the main advantage of ranked choice voting according to its supporters?\",\n      \"answer\": \"Encourages increased turnout and candidate participation and helps select more moderate candidates.\",\n      \"percent_through\": 35\n    },\n    {\n      \"question\": \"Which states currently use ranked choice voting statewide?\",\n      \"answer\": \"Alaska and Maine\",\n      \"percent_through\": 15\n    },\n    {\n      \"question\": \"Which three states are considering the adoption of ranked choice voting this year?\",\n      \"answer\": \"Idaho, Oregon, and Nevada\",\n      \"percent_through\": 20\n    },\n    {\n      \"question\": \"What modification to the voting process will Idaho and Nevada implement if they switch to ranked choice voting?\",\n      \"answer\": \"They will establish new open primaries to reduce the slate of candidates to four and five respectively.\",\n      \"percent_through\": 25\n    },\n    {\n      \"question\": \"What did the MIT Election Data Science Lab find about RCV in Maine?\",\n      \"answer\": \"It produced significantly lower levels of voter confidence, voter satisfaction, and ease of use.\",\n      \"percent_through\": 50\n    },\n    {\n      \"question\": \"Who did ranked choice voting help in Alaska in 2022?\",\n      \"answer\": \"Moderate Democrat Mary Peltola and moderate Republican Lisa Murkowski.\",\n      \"percent_through\": 65\n    },\n    {\n      \"question\": \"Why is Alaska considering repealing their ranked choice system?\",\n      \"answer\": \"Hard-liners see ranked choice voting as an existential threat to their politics.\",\n      \"percent_through\": 80\n    },\n    {\n      \"question\": \"How many jurisdictions around the country use ranked choice voting?\",\n      \"answer\": \"64 jurisdictions\",\n      \"percent_through\": 10\n    },\n    {\n      \"question\": \"What potential drawback does ranked choice voting have according to the article?\",\n      \"answer\": \"Swapping voting methods can sow confusion within the electorate.\",\n      \"percent_through\": 45\n    },\n    {\n      \"question\": \"What overall effect does ranked choice voting have on the selection of candidates?\",\n      \"answer\": \"It helps in the selection of more moderate candidates who earn the majority of the electorate's support.\",\n      \"percent_through\": 35\n    }\n  ]\n}"
            }
        }]
    }
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = valid_json
        response = generate_card_data(essay)
        assert response is not None
        is_created = create_cards(essay, response)
        assert is_created is True
        assert Card.objects.count() == 10
