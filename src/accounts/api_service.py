# ------------------ email validation --------------------
import json

import requests

from SnapCord.settings import EMAIL_VALIDATION_KEY


def emailvalidation(email):
    key = EMAIL_VALIDATION_KEY
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={key}&email={email}"
    response = requests.get(url=url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if data['deliverability'] == 'DELIVERABLE':
            return True
    return False
