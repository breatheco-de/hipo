import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_academy_technologies():
    
    endpoint = f"https://breathecode.herokuapp.com/v1/registry/academy/technology"
    headers = {
        "Authorization": f"Token {os.getenv('BREATHECODE_PERMANENT_TOKEN')}",
        "Academy": os.getenv("ACADEMY_ID")
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_technology_assets(technology: str):
    TECHNOLOGY_FILTER = f"?technologies={technology}"
    ASSET_TYPE_FILTER = "&asset_type=EXERCISE"
    VISIBILITY_FILTER = "&visibility=PUBLIC"
    endpoint = f"https://breathecode.herokuapp.com/v1/registry/asset{TECHNOLOGY_FILTER}{ASSET_TYPE_FILTER}{VISIBILITY_FILTER}"
    response = requests.get(endpoint)
    return response.json()


def get_ai_context(asset_id: str):
    endpoint= f"https://breathecode.herokuapp.com/v1/registry/asset/{asset_id}/context"
    headers = {
        "Authorization": f"Token {os.getenv('BREATHECODE_PERMANENT_TOKEN')}",
        "academy_id": os.getenv("ACADEMY_ID")
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

