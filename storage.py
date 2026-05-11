import json

RECORDS_FILE = "records.json"
SETTINGS_FILE = "settings.json"

def load_records():
    with open(RECORDS_FILE, "r") as file:
        return json.load(file)

def save_records(data):
    with open(RECORDS_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_settings():
    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)