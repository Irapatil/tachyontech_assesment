import requests
from config.settings import *

class SalesforceClient:

    def __init__(self):
        self.token = None
        self.instance_url = None
        self.authenticate()

    def authenticate(self):
        url = "https://login.salesforce.com/services/oauth2/token"

        payload = {
            "grant_type": "password",
            "client_id": SF_CLIENT_ID,
            "client_secret": SF_CLIENT_SECRET,
            "username": SF_USERNAME,
            "password": SF_PASSWORD

        }

        res = requests.post(url, data=payload).json()
        self.token = res.get("access_token")
        self.instance_url = res.get("instance_url")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_case(self, case_id):
        url = f"{self.instance_url}/services/data/v58.0/sobjects/Case/{case_id}"
        return requests.get(url, headers=self._headers()).json()

    def update_case(self, case_id, summary):
        url = f"{self.instance_url}/services/data/v58.0/sobjects/Case/{case_id}"

        payload = {
            "Description": summary
        }

        return requests.patch(url, json=payload, headers=self._headers())

    def create_task(self, case_id):
        url = f"{self.instance_url}/services/data/v58.0/sobjects/Task"
        payload = {
            "Subject": "Follow-up on Technical Fault",
            "WhatId": case_id,
            "Priority": "High"
        }

        return requests.post(url, json=payload, headers=self._headers())