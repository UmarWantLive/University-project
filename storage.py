import json
import os

RECORDS_FILE = "records.json"
HISTORY_FILE = "history.json"


def ensure_files_exist():
    if not os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "w") as file:
            json.dump({
                "best_score": 0,
                "matches_played": 0,
                "left_player_wins": 0,
                "right_player_wins": 0,
                "total_goals": 0
            }, file, indent=4)

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as file:
            json.dump([], file, indent=4)


def load_records():
    ensure_files_exist()

    with open(RECORDS_FILE, "r") as file:
        return json.load(file)


def save_records(data):
    with open(RECORDS_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_history():
    ensure_files_exist()

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(data):
    with open(HISTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_match_to_history(match_info):
    history = load_history()
    history.append(match_info)
    save_history(history)