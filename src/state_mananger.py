import json

def save_state(case_id, state):
with open(f"state_{case_id}.json", "w") as f:
json.dump(state, f)

def load_state(case_id):
try:
with open(f"state_{case_id}.json") as f:
return json.load(f)
except:
return None
