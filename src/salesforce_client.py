import requests

class SalesforceClient:
def __init__(self, access_token, instance_url):
self.access_token = access_token
self.instance_url = instance_url

def update_case(self, case_id, summary):
url = f"{self.instance_url}/services/data/v58.0/sobjects/Case/{case_id}"

headers = {
"Authorization": f"Bearer {self.access_token}",
"Content-Type": "application/json"
}

payload = {
"Technical_Summary__c": summary,
"Status": "In Progress"
}

return requests.patch(url, json=payload, headers=headers)

def create_task(self, case_id):
url = f"{self.instance_url}/services/data/v58.0/sobjects/Task"

headers = {
"Authorization": f"Bearer {self.access_token}",
"Content-Type": "application/json"
}

payload = {
"Subject": "Follow-up Task",
"WhatId": case_id,
"Priority": "High",
"Status": "Not Started"
}

return requests.post(url, json=payload, headers=headers)