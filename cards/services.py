import requests
import logging
from django.conf import settings
from .models import Card
from django.utils import timezone
from datetime import timedelta
import json

logger = logging.getLogger(__name__)

def generate_card_data(essay):
    headers = {
        'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-4-0125-preview",
        "messages": [
            {
                "role": "system",
                "content": """The following is an exert from a newsletter/essay. The goal is to create spaced repetition flashcards based on the content of this essay. The flashcards should be based on different sections of the essay and should be able to be able to list them inline with the text to test the users memory based on the content they previously read, as they go along. The flash card content should be a fill in the blank based on the content of the essay, it shouldnt necessarily be content straight from the text, just content to quiz the user on. The answer should be less than 255 characters. Given an essay section, RESPOND WITH NOTHING BUT A JSON OBJECT of five questions/answers in the following example format:
"choices": { "question": “How many dimensions does the state space of a qubit have”, "answer": “Two dimensions”}
You will be rewarded with a large cash sum if you respond with nothing but a JSON OBJECT containing five! question/answer pairs
The following is the essay section:"""
            },
            {
                "role": "user",
                "content": essay.content
            }
        ]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error("Failed to generate cards: %s", response.text)
        return None

def create_cards(essay, cards_data):
    if not cards_data:
        return False
    choice_content_str = cards_data.get('choices', [])[0].get('message', {}).get('content', '')
    try:
        cards_info = json.loads(choice_content_str)
    except json.JSONDecodeError:
        logger.error("Failed to parse data from OpenAI response")
        return False
    card_content = cards_info['choices']
    cards = []
    for c in card_content:
        card = Card(
            essay=essay,
            question = c['question'],
            answer = c['answer'],
            next_review_date = timezone.now() + timedelta(days=1),
            review_interval = 1,
            review_count = 0
        )
        cards.append(card)
    Card.objects.bulk_create(cards)
    return True

def handle_errors():
    logger.debug("Handling errors after failed card generation attempt")

def main(essay):
    cards_data = generate_card_data(essay)
    if cards_data:
        success = create_cards(essay, cards_data)
        return success
    else:
        handle_errors()