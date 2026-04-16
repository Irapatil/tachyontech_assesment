import json

def save_failure(case_id, error):
    with open("failures.json", "a") as f:
        f.write(json.dumps({"case_id": case_id, "error": error}) + "\n")
