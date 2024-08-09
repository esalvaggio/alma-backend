import requests
import logging
from django.conf import settings
from .models import Card
from django.utils import timezone
from datetime import timedelta
import json
from .config import Config

logger = logging.getLogger(__name__)

def generate_card_data(essay):
    headers = {
        'Authorization': f'Bearer {Config.OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": """The following is an excerpt from a newsletter/essay. The goal is to create spaced repetition flashcards based on the content of this essay. The flashcards should be based on different sections of the essay and should make sense when listed inline the text to test the users memory based on the content they previously read, as they go along. The cards should also make sense on their own without the text as context, as they will be reviewed later. The flash card content should be fill-in-the-blank based on the content of the essay. The focus shouldn't necessarily be less on specific words used or sentances in the text unless that's relevant, the focus should be on choosing content or topics to quiz the user on that if remembered, will help you remember the piece as a whole, as well as the most useful information to retain to help you better learn the underlying concepts. 
 The answer should be less than 255 characters. I also want you to specify as a percentage, how far down the page the question should be displayed. Questions should be displayed after (but not necessarily immediately after) the information they relate to, embedded in the text.  Given an essay section, RESPOND WITH NOTHING BUT A JSON OBJECT of five questions/answers in the following example format:
"questions": { "question": “How many dimensions does the state space of a qubit have”, "answer": "Two dimensions", "percent_through": 30}
You will be rewarded if you respond with nothing but a JSON OBJECT containing no more than 10 question/answer pairs. The number of question/answer pairs should be dependent on how the minimum number of flashcards necessary to help the user understand what they've read. Add in 2 difficult question/answer pairs that are more about general concepts presented in the article to list at the end of the article to test if the reader retained the overall message
The following is the essay section: """
            },
            {
                "role": "user",
                "content": essay.content
            }
        ]
    }
    response = requests.post(Config.OPENAI_ENDPOINT, json=data, headers=headers)
    if response.status_code == 200:
        logger.info("Raw response text: %s", response.text)  
        logger.info("Successful OpenAI response: %s", response.json())
        return response.json()
    else:
        logger.error("Failed to generate cards: %s", response.text)
        return None


def create_cards(essay, cards_data):
    if not cards_data:
        return False
    if "choices" not in cards_data:
        logger.error(f"Expected 'choices' in response but did not find it")
        return False
    try:
        cards_info = json.loads(cards_data.get('choices', [])[0].get('message', {}).get('content', ''))
        logger.info("Successfully parse cards response: %s", cards_info)
    except json.JSONDecodeError:
        logger.error("Failed to parse data from OpenAI response")
        return False
    except IndexError:
        logger.error("The questions array was empty")
        return False
    cards = []
    for c in cards_info['questions']:
        card = Card(
            user = essay.user,
            essay=essay,
            question = c['question'],
            answer = c['answer'],
            percent_through = int(c['percent_through']),
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