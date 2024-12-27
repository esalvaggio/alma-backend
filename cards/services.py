import requests
import logging
from django.conf import settings
from .models import Card
from django.utils import timezone
from datetime import timedelta
import json
from .config import Config

logger = logging.getLogger(__name__)

# can i turn off data logging (don't train your model with this content)
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
                "content": """You are an assistant that generates spaced repetition flashcards based on an essay section. The flashcards should be based on different sections of the essay and make sense both inline and standalone if reviewed without the text. They should be fill-in-the-blank or general questions and focus on key concepts, not necessarily individual words or numbers unless very relevant, to help the user remember the piece as a whole, as well as retain the underlying concepts presented in the piece. Answers should be less than 255 characters. Specify a decimal 'percent_through' to indicate where in the essay the question should appear, with a 10-15% padding as to not risk displaying the card before the user has read the content. Include a final, more challenging question to test overall understanding. Return no more than 10 question/answer pairs, adjusting the number of returned pairs based on the length of the article, if shortreturn few pairs. """
            },
            {
                "role": "user",
                "content": essay.content
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "flashcard_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                    "questions": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "properties": {
                            "question": {
                            "type": "string",
                            "description": "The flashcard question."
                            },
                            "answer": {
                            "type": "string",
                            "description": "The answer to the flashcard question."
                            },
                            "percent_through": {
                            "type": "number",
                            "description": "Percentage through the essay where the question should appear."
                            }
                        },
                        "required": ["question", "answer", "percent_through"],
                        "additionalProperties": False
                        }
                    }
                },
                "required": ["questions"],
                "additionalProperties": False
                }
            }
        }
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
    choices = cards_data.get('choices', [])
    if not choices:
        logger.error(f"Expected 'choices' in response but did not find it")
        return False
    message = choices[0].get('message', {})
    if 'refusal' in message and message['refusal'] != None:
        logger.error(f"Assistant refused the request: {message['refusal']}")
        return False
    content = message.get('content', {})
    if not content:
        logger.error("No 'content' field found in the assistant's message.")
        return False
    try:
        cards_info = json.loads(content)
        logger.info("Successfully parse cards response: %s", cards_info)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON from 'content': {e}")
        return False
    except IndexError:
        logger.error("The questions array was empty")
        return False
    cards = []
    for c in cards_info['questions']:
        try:
            card = Card(
                user = essay.user,
                essay=essay,
                question = c['question'],
                answer = c['answer'],
                percent_through = int(c['percent_through'] * 100),
                next_review_date = timezone.now(),
                review_interval = 1,
                review_count = 0
            )
            cards.append(card)
        except KeyError as e:
            logger.error(f"Missing expected key in question data: {e}")
            continue
        except ValueError as e:
            logger.error(f"Invalid data type in question data: {e}")
            continue
    if not cards:
        logger.error("No valid cards were created.")
        return False
    Card.objects.bulk_create(cards)
    logger.info(f"Successfully created {len(cards)} cards.")
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