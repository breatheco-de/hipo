import requests
from dotenv import load_dotenv
import os


FOUR_GEEKS_WEB_HOST = "https://4geeks.com"
"""
const connectorsDict = {
  EVENT: 'workshops',
  LESSON: 'lesson',
  EXERCISE: 'interactive-exercise',
  PROJECT: 'interactive-coding-tutorial',
  ARTICLE: 'how-to',
};
"""

load_dotenv()


def get_academy_technologies():

    endpoint = f"https://breathecode.herokuapp.com/v1/registry/academy/technology"
    headers = {
        "Authorization": f"Token {os.getenv('BREATHECODE_PERMANENT_TOKEN')}",
        "Academy": os.getenv("ACADEMY_ID"),
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def is_not_english(language: str):
    return language != "us" and language != "en"


def make_url(asset_type: str, asset_slug: str, language: str = "us"):

    connectorsDict = {
        "EVENT": "workshops",
        "LESSON": "lesson",
        "EXERCISE": "interactive-exercise",
        "PROJECT": "interactive-coding-tutorial",
        "ARTICLE": "how-to",
    }

    language_section = ""
    if is_not_english(language):
        language_section = f"{language}/"

    return f"{FOUR_GEEKS_WEB_HOST}/{language_section}{connectorsDict[asset_type]}/{asset_slug}"


def get_technology_assets(technology: str):
    TECHNOLOGY_FILTER = f"?technologies={technology}"
    ASSET_TYPE_FILTER = "&asset_type=EXERCISE"
    VISIBILITY_FILTER = "&visibility=PUBLIC"

    endpoint = f"https://breathecode.herokuapp.com/v1/registry/asset{TECHNOLOGY_FILTER}{ASSET_TYPE_FILTER}{VISIBILITY_FILTER}"
    response = requests.get(endpoint)
    return response.json()


def get_ai_context(asset_id: str):
    endpoint = f"https://breathecode.herokuapp.com/v1/registry/asset/{asset_id}/context"
    headers = {
        "Authorization": f"Token {os.getenv('BREATHECODE_PERMANENT_TOKEN')}",
        "academy_id": os.getenv("ACADEMY_ID"),
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()
