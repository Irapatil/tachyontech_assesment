import requests
from config.settings import SLACK_WEBHOOK

def send_alert(message):
    if SLACK_WEBHOOK:
        requests.post(SLACK_WEBHOOK, json={"text": message})